from flask import Flask, render_template, request, redirect, flash, url_for, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db, init_db
import os

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

@app.route('/', methods = ['GET'])
def home():
    auth()
    db = init_db()
    posts = db.execute("SELECT * FROM post JOIN user ON post.author_id = user.id ORDER BY created DESC")
    return render_template('home.html', posts=posts)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                con.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
                con.commit()
            except con.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("login"))
        flash(error)
    return render_template('register.html')
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = get_db()
        error = None
        user = con.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        if user is None:
            error = 'Invalid username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        flash(error)
    return render_template("login.html")

def auth():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    auth()
    if g.user:
        con = get_db()
        posts = con.execute("SELECT * FROM post JOIN user ON post.author_id = user.id WHERE user.id = ? ORDER BY created DESC", (g.user['id'],)).fetchall()
        return render_template('dashboard.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/create', methods=('GET', 'POST'))
def create():
    auth()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = "Don't forget to add a title."
        if error is not None:
            flash(error)
        else:
            con = get_db()
            con.execute("INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)", (g.user['id'], title, body))
            con.commit()
            return redirect(url_for('dashboard'))
    return render_template('create.html')

def get_post(id):
    auth()
    post = get_db().execute("SELECT post.id, title, body, created, author_id, username FROM post JOIN user ON post.author_id = user.id WHERE post.id = ?", (id,)).fetchone()
    return post

@app.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = "Don't forget to add a title."
        if error is not None:
            flash(error)
        else:
            con = get_db()
            con.execute("UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id))
            con.commit()
            return redirect(url_for('dashboard'))
    return render_template('update.html', post=post)

@app.route('/<int:id>/delete', methods = ['POST'])
def delete(id):
    get_post(id)
    con = get_db()
    con.execute("DELETE FROM post WHERE id = ?", (id,))
    con.commit()
    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
