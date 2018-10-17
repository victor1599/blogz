from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Miami2020@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)     
    title = db.Column(db.String)  
    post = db.Column(db.Text)   

    def __init__(self, title, post):
        self.title = title
        self.post = post

@app.route("/")
def index():
    return redirect("/blog")

@app.route('/blog')
def show_blog():
    post_id = request.args.get('id')
    if (post_id):
        show_post = Blog.query.get(post_id)
        return render_template('show_post.html', show_post=show_post)
    else:
        all_blog_posts = Blog.query.all()
        return render_template('blog.html', posts=all_blog_posts)

def empty(x):
    if x:
        return True
    else:
        return False

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

if __name__== '__main__':
    app.run()