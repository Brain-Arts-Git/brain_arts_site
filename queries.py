#!usr/bin/env python3
from slugify import slugify
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


def get_blog_posts(page):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, link_name, author, DATE_FORMAT(date_published, "%M %e, %Y") AS date_published, img_id, content, date_published AS unformatted_date FROM blog_posts ORDER BY unformatted_date DESC;'
		cursor.execute(query)
		posts = cursor.fetchall()

	connection.close()

	for post in posts:
		# decoding only needed for production
		try:
			# decode utf8 content
			post['title'] = post['title'].decode('utf-8')
			post['content'] = post['content'].decode('utf-8')
			post['author'] = post['author'].decode('utf-8')
		except:
			pass
		# only show first 500 characters of each post
		post['content'] = markdown2.markdown(post['content'][0:500].replace('#', '')+'...')

	# return 10 posts per page
	if page < 2:
		return posts[0:10]
	else:
		first_post = (page * 10) - 10
		last_post = first_post + 10

	return posts[first_post:last_post]


def get_post(link_name):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT id, title, link_name, author, DATE_FORMAT(date_published, "%%M %%e, %%Y") AS date_published, img_id, content AS html_content, content FROM blog_posts WHERE link_name = %s;'
		cursor.execute(query, (link_name))
		post = cursor.fetchone()

	connection.close()

	# decoding only needed for production
	try:
		# decode utf8 content
		post['title'] = post['title'].decode('utf-8')
		post['content'] = post['content'].decode('utf-8')
		post['html_content'] = post['html_content'].decode('utf-8')
		post['author'] = post['author'].decode('utf-8')
	except:
		pass

	# convert markdown to html
	post['html_content'] = markdown2.markdown(post['html_content'])

	return post


def create_blog_post(title, author, date_published, img_id, content):
	connection = db_login()

	link_name = slugify(title)

	with connection.cursor() as cursor:
		query = 'INSERT INTO blog_posts (title, link_name, author, date_published, img_id, content) VALUES (%s, %s, %s, %s, %s, %s);' 
		cursor.execute(query, (title, link_name, author, date_published, img_id, content))

	connection.close()


def update_blog_post(post_id, title, author, content):
	connection = db_login()

	link_name = slugify(title)

	with connection.cursor() as cursor:
		query = 'UPDATE blog_posts SET title = %s, link_name = %s, author = %s, content = %s WHERE id = %s;'
		cursor.execute(query, (title, link_name, author, content, post_id))

	connection.close()

	return link_name


def get_img_id():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT max(id) AS "id" FROM img_ids;'
		cursor.execute(query)
		max_id = cursor.fetchone()

		if max_id['id'] is not None:
			next_id = int(max_id['id']) + 1
		else:
			next_id = 1

		query = 'INSERT INTO img_ids (id) VALUES (' + str(next_id) + ');'
		cursor.execute(query)

	connection.close()

	return next_id


def get_current_img_id(post_id):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT img_id FROM blog_posts WHERE id = %s;'
		cursor.execute(query, (post_id))
		img_id = cursor.fetchone()

	connection.close()

	return img_id['img_id']




def get_services():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, link_name, signup_link, DATE_FORMAT(date_published, "%M %e, %Y") AS date_published, img_id, content, date_published AS unformatted_date FROM services ORDER BY unformatted_date DESC;'
		cursor.execute(query)
		services = cursor.fetchall()

	connection.close()

	for service in services:
		# decoding only needed for production
		try:
			# decode utf8 content
			service['title'] = service['title'].decode('utf-8')
			service['content'] = service['content'].decode('utf-8')
			service['author'] = service['author'].decode('utf-8')
		except:
			pass
		# only show first 500 characters of each service
		service['content'] = markdown2.markdown(service['content'][0:500].replace('#', '')+'...')

	return services

def create_service(title, signup_link, date_published, img_id, content):
	connection = db_login()

	link_name = slugify(title)

	with connection.cursor() as cursor:
		query = 'INSERT INTO services (title, link_name, signup_link, date_published, img_id, content) VALUES (%s, %s, %s, %s, %s, %s);' 
		cursor.execute(query, (title, link_name, signup_link, date_published, img_id, content))

	connection.close()

def get_service(link_name):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT id, title, link_name, signup_link, DATE_FORMAT(date_published, "%%M %%e, %%Y") AS date_published, img_id, content AS html_content, content FROM services WHERE link_name = %s;'
		cursor.execute(query, (link_name))
		service = cursor.fetchone()

	connection.close()

	# decoding only needed for production
	try:
		# decode utf8 content
		service['title'] = service['title'].decode('utf-8')
		service['content'] = service['content'].decode('utf-8')
		service['html_content'] = service['html_content'].decode('utf-8')
		service['signup_link'] = service['signup_link'].decode('utf-8')
	except:
		pass

	# convert markdown to html
	service['html_content'] = markdown2.markdown(service['html_content'])

	return service	

def update_service(service_id, title, signup_link, content):
	connection = db_login()

	link_name = slugify(title)

	with connection.cursor() as cursor:
		query = 'UPDATE services SET title = %s, link_name = %s, signup_link = %s, content = %s WHERE id = %s;'
		cursor.execute(query, (title, link_name, signup_link, content, service_id))

	connection.close()

	return link_name	

def get_service_img_id():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT max(id) AS "id" FROM service_img_ids;'
		cursor.execute(query)
		max_id = cursor.fetchone()

		if max_id['id'] is not None:
			next_id = int(max_id['id']) + 1
		else:
			next_id = 1

		query = 'INSERT INTO service_img_ids (id) VALUES (' + str(next_id) + ');'
		cursor.execute(query)

	connection.close()

	return next_id


def get_current_service_img_id(service_id):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT img_id FROM services WHERE id = %s;'
		cursor.execute(query, (service_id))
		img_id = cursor.fetchone()

	connection.close()

	return img_id['img_id']	