from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL # type: ignore
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (title) VALUES (%s)", [title])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tasks WHERE id = %s", [id])
    task = cur.fetchone()
    cur.close()
    if request.method == 'POST':
        title = request.form['title']
        completed = 'completed' in request.form
        cur = mysql.connection.cursor()
        cur.execute("UPDATE tasks SET title = %s, completed = %s WHERE id = %s", (title, completed, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete_task(id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET completed = %s WHERE id = %s", (True, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)