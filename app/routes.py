from flask import Flask, render_template, session, redirect, url_for, request, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from app import app
import os

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = os.urandom(16)

# user model
class User(UserMixin):
	def __init__(self, id):
		self.id = id
		self.name = 'admin'
		self.password = open('admin.login', 'r').read()
		
	def __repr__(self):
		return "%d/%s/%s" % (self.id, self.name, self.password)

myUser = User(666)

@login_manager.user_loader
def load_user(user_id):
	return User(user_id)

@app.route('/admin', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == 'admin' and password == open('admin.login', 'r').read():
			id = 666
			user = User(id)
			login_user(user)
			return render_template('admin.html')
		else:
			return abort(401)
	else:
		return render_template('admin.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect('/login')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog')
def blog():
	# TODO: fn to query for blog posts
	return render_template('blog.html')

@app.route('/post')
def post():
	return render_template('post.html')

@app.route('/dn4s')
def dn4s():
	return render_template('dn4s.html')

@app.route('/no_fucker')
def no_fucker():
	return render_template('no_fucker.html')
