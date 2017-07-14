import os
from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'abc123'


#to render changes to css etc. in real time, instead of relying on possibly old, outdated caches
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
    #     title = request.form['title']
    #     body = request.form['body']
    #     return render_template('blog.html', title=title, body=body)

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('blog.html', post=post)

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    error = None

    if request.method == "POST":
        blog_title = request.form['title']
        blog_body = request.form['body']
        blog_id = request.form['blog_id']

        if (not blog_title) and (not blog_body):
            error = "empty_blog_error"
            return render_template('newpost.html', error=error, title=blog_title, body=blog_body)
        elif (not blog_body):
            error = "body_error"
            return render_template('newpost.html', error=error, title=blog_title, body=blog_body)
        elif (not blog_title):
            error = "title_error"
            return render_template('newpost.html', error=error, title=blog_title, body=blog_body)

        elif error == None:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect("/blog?id=" + str(new_blog.id))
            # return render_template('blog.html', blog=new_blog)
    return render_template('newpost.html', error=error)


@app.route('/')
def index():
    return redirect('/blog')

if __name__ == "__main__":
    app.run()
