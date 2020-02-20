#!usr/bin/env python3
import markdown2
import pymysql

# database functions

def db_login():
	# TODO: read login credentials
	with open('login.secure', 'r') as f:
		user = next(f).strip()
		pswd = next(f).strip()

	# connect to database
	connection = pymysql.connect(host='localhost', user=user, passwd=pswd, db='brain-arts', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

	return connection


def admin_login(username, password):
	connection = db_login()
	with connection.cursor() as cursor:
		query = 'SELECT username, password FROM admin WHERE username = "' + username + '";'
		cursor.execute(query)
		login_info = cursor.fetch()

	connection.close()

	if login_info['password'] == password:
		return True
	else:
		return False


def get_blog_posts():
	connection = db_login()

	with connection.cursor() as cursor:
		query = 'SELECT title, author, date_published, img_link, content FROM blog_posts ORDER BY date_published;'
		cursor.execute(query)
		posts = cursor.fetchall()

	connection.close()

	return posts


def create_blog_post(title, author, date_published, img_link, content):
	connection = db_login()

	# convert markdown to html
	html_content = markdown2.markdown(content)

	with connection.cursor() as cursor:
		query = 'INSERT INTO blog_posts (title, author, date_published, img_link, content) VALUES (%s, %s, %s, %s, %s);' 
		cursor.execute(query, (title, author, date_published, img_link, html_content))
		posts = cursor.fetchall()

	connection.close()

	return posts


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
		query = 'INSERT INTO event_listings (event_name, event_venue, event_time) VALUES ({0}, {1}, {2});'
			.format(event_name, event_venue, event_time)
		# TODO: probably need try except in case this fails
		cursor.execute(query)

	connection.close()

	return 'Event Created!'
