from flask import Flask, render_template, request, redirect
import MySQLdb

app = Flask(__name__)

# ✅ Database Configuration (Inline)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'samiha'  # Replace with your real password
app.config['MYSQL_DB'] = 'flask_crud_db'

# ✅ Connect to MySQL
def get_db():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    db.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    name = request.form['name']
    email = request.form['email']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit_user(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    db.close()
    return render_template('edit_user.html', user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    name = request.form['name']
    email = request.form['email']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, id))
    db.commit()
    db.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_user(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    db.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
