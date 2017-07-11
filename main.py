import os
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# app.secret_key = 'abc123'

""" Inspired by http://flask.pocoo.org/snippets/40/ """
@app.url_defaults
def hashed_url_for_static_file(endpoint, values):
    if 'static' == endpoint or endpoint.endswith('.static'):
        filename = values.get('filename')
        if filename:
            if '.' in endpoint:  # has higher priority
                blueprint = endpoint.rsplit('.', 1)[0]
            else:
                blueprint = request.blueprint  # can be None too

            if blueprint:
                static_folder = app.blueprints[blueprint].static_folder
            else:
                static_folder = app.static_folder

            param_name = 'h'
            while param_name in values:
                param_name = '_' + param_name
            values[param_name] = static_file_hash(os.path.join(static_folder, filename))

def static_file_hash(filename):
  return int(os.stat(filename).st_mtime) # or app.config['last_build_timestamp'] or md5(filename) or etc...



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=["POST", "GET"])
def blog():
    # if request.method == "POST":
    #     blog_title = request.form['title']
    #     blog_body = request.form['body']
    #     new_blog = Blog(title, body)
    #     db.session.add(new_blog)
    #     db.session.commit()
    # if request.method == "POST":
    #     blog_id = request.form['blog-id']
    #     return redirect("/?blog=" + blog_id)
    #  if request.method == "GET":
    #      title = request.form['title']
    #      body = request.form['body']
    #      return render_template('/blog', title=title
    # if request.method == "POST":
    #      blog_id = int(request.form['blog-id'])
    #      blog = Blog.query.get(blog_id)
    #      return render_template('/blog.html', blog=blog)
        #  show_blog = Blog.query.filter_by().all()
    #     return redirect("/?blog=" + blog_id)
    if request.method == "POST":
        title = request.form['title']
        body = request.form['body']
        return render_template('blog.html', title=title, body=body)

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == "POST":
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/')

    blogs = Blog.query.all()

    return render_template('newpost.html')
    # return redirect('/')

# @app.route('/newpost', methods=['POST', 'GET'])
# def new_post():
    # after submitting, redirects to main Blog page
    #if blog title or blog body is left empty, the form is rendered again with a helpful error message, and it retains the previously entered inputs
    # return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()

    return render_template('blog.html', title="Build A Blog", blogs=blogs)

if __name__ == "__main__":
    app.run()
