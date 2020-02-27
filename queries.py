#!usr/bin/env python3
import markdown2
import pymysql

# database functions

def db_login():
	with open('db.login', 'r') as f:
		user = next(f).strip()
		pswd = next(f).strip()

	# connect to database
	connection = pymysql.connect(host='localhost', user=user, passwd=pswd, db='brain_arts', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

	return connection


def get_blog_posts():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, author, date_published, img_id, content FROM blog_posts ORDER BY date_published;'
		cursor.execute(query)
		posts = cursor.fetchall()

	connection.close()

	for post in posts:
		# only show first 500 characters of each post
		post['content'] = post['content'][0:500]

	return posts

def get_post(title):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, author, date_published, img_id, content FROM blog_posts WHERE title = %s;'
		cursor.execute(query, (title))
		post = cursor.fetchall()

	connection.close()

	# convert markdown to html
	post['content'] = markdown2.markdown(post['content'])

	return post


def create_blog_post(title, author, date_published, img_id, content):
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'INSERT INTO blog_posts (title, author, date_published, img_id, content) VALUES (%s, %s, %s, %s, %s);' 
		cursor.execute(query, (title, author, date_published, img_id, content))
		posts = cursor.fetchall()

	connection.close()

	return posts


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


# TODO: these remaining functions will be used for non gcal event listings
def get_event_listings():
	connection = db_login()
	
	with connection.cursor() as cursor:
		query = 'SELECT event_name, event_venue, event_time FROM event_listings ORDER BY event_time LIMIT 10;'
		cursor.execute(query)
		events = cursor.fetchall()

	connection.close()

	return events


def create_event_listing(event_name, event_time, event_location):
	connection = db_login()

	with connection.cursor() as cursor:
		# TODO: need to escape user input to prevent sql injection
		query = 'INSERT INTO event_listings (event_name, event_venue, event_time) VALUES ({0}, {1}, {2});'.format(event_name, event_venue, event_time)
		# TODO: probably need try except in case this fails
		cursor.execute(query)

	connection.close()

	return 'Event Created!'
