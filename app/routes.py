from flask import Flask, render_template, session, redirect, url_for, request, abort, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
from datetime import datetime
from app import app
import queries, os

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = os.urandom(16)

UPLOAD_FOLDER = 'app/static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# user model
class User(UserMixin):
	def __init__(self, id):
		self.id = id
		self.name = 'admin'
		self.password = open('/var/www/brain_arts_site/admin.login', 'r').read().strip()

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
		if username == 'admin' and password == open('/var/www/brain_arts_site/admin.login', 'r').read().strip():
			id = 666
			user = User(id)
			login_user(user)
			return redirect('/create_post')
		else:
			return abort(401)
	else:
		return render_template('admin.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect('/admin')

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/blog')
def blog():
	link_name = request.args.get('post')
	if link_name != None:
		post = queries.get_post(link_name)
		return render_template('post.html', post=post)
	else:
		posts = queries.get_blog_posts()
		return render_template('blog_posts.html', posts=posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
	if request.method == 'POST':
		# TODO: need to either show error or change behavior
		# check if the post request has the file part
		if 'file' not in request.files:
			print('No file part')
			return redirect('/create_post')

		file = request.files['file']

		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect('/create_post')
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			img_id = queries.get_img_id()
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(img_id)))

		title = request.form['title']
		author = request.form['author']
		content = request.form['content']
		date_published = datetime.today().strftime('%Y-%m-%d')
		queries.create_blog_post(title, author, date_published, img_id, content)
		return redirect('/blog')
	else:
		return render_template('create_post.html')

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_post():
	if request.method == 'POST':
		file = request.files['file']
		title = request.form['title']
		author = request.form['author']
		content = request.form['content']
		post_id = request.form['post_id']

		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			img_id = queries.get_current_img_id(post_id)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(img_id)))

		date_published = datetime.today().strftime('%Y-%m-%d')
		link_name = queries.update_blog_post(post_id, title, author, content)
		return redirect('/blog?post='+link_name)
	else:
		link_name = request.args.get('post')
		post = queries.get_post(link_name)
		return render_template('edit_post.html', post=post)

@app.route('/dn4s')
def dn4s():
	return render_template('dn4s.html')

@app.route('/no_fucker')
def no_fucker():
	return render_template('no_fucker.html')
