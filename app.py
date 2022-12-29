import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from helpers import login_required

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts JOIN users ON posts.user = users.user_id WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = '6c89336bd226723485d418d19d930ad97092448b403769bcfefc18872dcff517'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts JOIN users ON posts.user = users.user_id').fetchall()
    # users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template("index.html", posts=posts)


@app.route('/<int:post_id>')
@login_required
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        
        elif not content:
            flash('Content is required!')
        
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (user, title, content) VALUES (?, ?, ?)',
                         (session["user_id"], title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('create.html') 

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        conn = get_db_connection()
        usernames = conn.execute("SELECT username FROM users").fetchall()
        conn.close()

        username_list = []

        for i in range(len(usernames)):
            username_list.append(usernames[i]["username"])

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            # abort(400)
            flash("Username is required")
            return render_template("register.html")

        elif username in username_list:
            # abort(400)
            flash("Username is taken")
            return render_template("register.html")

        elif not password or not confirmation:
            flash("Enter password and confirmation")
            return render_template("register.html")
            # abort(400)

        elif password != confirmation:
            flash("passwords do not match")
            return render_template("register.html")
            # abort(400)
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)))

            user = conn.execute("SELECT user_id FROM users WHERE username=?", (username,)).fetchone()
            conn.commit()
            conn.close()
            session["user_id"] = user["user_id"]
            return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        conn = get_db_connection()
        usernames = conn.execute("SELECT username FROM users").fetchall()
        conn.close()

        username_list = []

        for i in range(len(usernames)):
            username_list.append(usernames[i]["username"])
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Username is required")
            return render_template("login.html")
            # abort(400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Password is required")
            return render_template("login.html")

        elif not request.form.get("username") in username_list:
            flash("Username is invalid")
            return render_template("login.html")
            # return flash("must provide password")

        # Query database for username
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
        conn.close()
        # Ensure username exists and password is correct
        if not check_password_hash(rows["hash"], request.form.get("password")):
            flash("Incorrect password")
            return render_template("login.html")
            # return flash("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")