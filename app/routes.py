from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    # TODO: fn to query for blog posts
    return render_template('blog.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
