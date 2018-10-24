from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import traceback

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Miami2020@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)     
    title = db.Column(db.String(40))  
    post = db.Column(db.Text(120))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id")) 

    def __init__(self, title, post):
        self.title = title
        self.post = post
        self.author_id = author_id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    blogs = db.relationship("Blog", backref="author")
    logged_in = db.Column(db.Boolean())

    def __init__(self, username, password, email):
        self.email = email
        self.username = username
        self.password = password

@app.route("/", methods=['GET','POST'])
def index():
    blogs = None
    all_blogs = Blog.query.all()

    data_tuples = []

    user = None
    try:
        if session['logged_in']:
            blogs = Blog.query.filter(User.id == session["author_id"])
        else:
            pass
    except KeyError:
        pass

    for blog in all_blogs:
        author_object = User.query.get(blog.author_id)
        author_username = author_object.username
        object_tuple=(blog.title, blog.id, author_username)
        data_tuples.append(object_tuple)
    return render_template('blogs.html', title="Dom's Safe Space", blogs=blogs, user=user, data_tuples=data_tuples)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(User.username == username).first()
        print(user)
        print(user.password)
        print(password)
        if user.password == password:
            session['logged_in'] = True
            session['author_id'] = user.id
            print(session)
            flash('Welcome')
            return render_template("blogs.html", user=user)
        else:
            flash("Error: Try again because you do not have login")
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)

@app.route('/signup', methods=['POST', 'GET'])
def register():

    password_error = None
    username_error = None
    email_error = None

    if request.method == 'POST':
        print(type(request.form))
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        username = request.form['username']
        existing_user = User.query.filter_by(email=email).first()
        existing_username = User.query.filter_by(username=username).first()
        print(existing_user)
        print(existing_username)
        if not existing_user and not existing_username:
            new_user = User(username, password, email)
            db.session.add(new_user)
            db.session.commit()
            print(new_user)
            return redirect('/login')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html', password_error=password_error, username_error=username_error, email_error=email_error)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    if request.method == 'POST':

        title_error = ""
        blog_error = ""

        post_title = request.form['blog_title']
        post_entry = request.form['blog_post']
        post_new = Blog(post_title, post_entry)

        if empty(post_title) and empty(post_entry):
            db.session.add(post_new)
            db.session.commit()
            post_link = "/blog?id=" + str(post_new.id)
            return redirect(post_link)
        else:
            if not empty(post_title) and not empty(post_entry):
                title_error = "Please enter text for blog title"
                blog_error = "Please enter text for blog entry"
                return render_template('newpost.html', blog_error=blog_error, title_error=title_error)
            elif not empty(post_title):
                title_error = "Please enter text for blog title"
                return render_template('newpost.html', title_error=title_error, post_entry=post_entry)
            elif not empty(post_entry):
                blog_error = "Please enter text for blog entry"
                return render_template('newpost.html', blog_error=blog_error, post_title=post_title)
    else:
        return render_template('newpost.html')

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return render_template("blogs.html")

@app.route("/blog/<blog_id>/", methods=['GET'])
def individual_entry(blog_id):
    blog = Blog.query.filter(blog_id).first()
    user = User.query.get(session['author_id'])

    return render_template("individual_entry.html",blog=blog, user=user)

app.secret_key='Dom is so awesome3143275434'


def empty(x):
    if x:
        return True
    else:
        return False

if __name__== '__main__':
    app.run()