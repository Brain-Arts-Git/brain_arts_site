#!usr/bin/env python3
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