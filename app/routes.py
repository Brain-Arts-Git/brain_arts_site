from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    # TODO: fn to query for blog posts
    return render_template('blog.html')

@app.route('/dn4s')
def dn4s():
	return render_template('dn4s.html')

@app.route('/no_fucker')
def no_fucker():
	return render_template('no_fucker.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
