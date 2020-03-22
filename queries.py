#!usr/bin/env python3
from app import app
import markdown2
import pymysql

# database functions

def db_login():
	# set paths for current env
	if app.config['DEBUG'] == True:
		db_login_path = '.db_login'
	else:
		db_login_path = '/var/www/brain_arts_site/.db_login'

	with open(db_login_path, 'r') as f:
		user = next(f).strip()
		pswd = next(f).strip()

	# connect to database
	connection = pymysql.connect(host='localhost', user=user, passwd=pswd, db='brain_arts', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

	return connection


def get_blog_posts():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, link_name, author, DATE_FORMAT(date_published, "%M %e, %Y") as date_published, img_id, content FROM blog_posts ORDER BY date_published;'
		cursor.execute(query)
		posts = cursor.fetchall()

	connection.close()

	for post in posts:
		# only show first 500 characters of each post
		post['content'] = markdown2.markdown(post['content'][0:500].replace('#', '')+'...')

	return posts


def get_post(link_name):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT id, title, link_name, author, DATE_FORMAT(date_published, "%%M %%e, %%Y") AS date_published, img_id, content AS html_content, content FROM blog_posts WHERE link_name = %s;'
		cursor.execute(query, (link_name))
		post = cursor.fetchone()

	connection.close()

	# convert markdown to html
	post['html_content'] = markdown2.markdown(post['html_content'])

	return post


def create_blog_post(title, author, date_published, img_id, content):
	connection = db_login()

	link_name = title.replace(' ', '_')

	with connection.cursor() as cursor:
		query = 'INSERT INTO blog_posts (title, link_name, author, date_published, img_id, content) VALUES (%s, %s, %s, %s, %s, %s);' 
		cursor.execute(query, (title, link_name, author, date_published, img_id, content))

	connection.close()


def update_blog_post(post_id, title, author, content):
	connection = db_login()

	link_name = title.replace(' ', '_')

	with connection.cursor() as cursor:
		query = 'UPDATE blog_posts SET title = %s, link_name = %s, author = %s, content = %s WHERE id = %s;'
		cursor.execute(query, (title, link_name, author, content, post_id))

	connection.close()

	return link_name


def get_img_id():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT max(img_id) AS "id" FROM blog_posts;'
		cursor.execute(query)
		max_id = cursor.fetchone()

	connection.close()

	if max_id['id'] is not None:
		next_id = int(max_id['id']) + 1
	else:
		next_id = 1

	return next_id

def get_current_img_id(post_id):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT img_id FROM blog_posts WHERE id = %s;'
		cursor.execute(query, (post_id))
		img_id = cursor.fetchone()

	connection.close()

	return img_id['img_id']
