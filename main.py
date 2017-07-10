from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# app.secret_key = 'abc123'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))



# @app.route('/blog')
# def blog():
    # display all blogs

# @app.route('/newpost', methods=['POST', 'GET'])
# def new_post():
    # after submitting, redirects to main Blog page
    #if blog title or blog body is left empty, the form is rendered again with a helpful error message, and it retains the previously entered inputs
    # return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('blog.html')
    # if request.method == 'POST':
    #     blog_entry = request.form['blog']


if __name__ == "__main__":
    app.run()
