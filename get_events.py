#!usr/bin/env python3
import pymysql

# script to pull event info from mysql - Jon

if __name__ == '__main__':
	# TODO: read login credentials
	with open('login.secure', 'r') as f:
		user = next(f).strip()
		pswd = next(f).strip()
	# connect to database
	connection = pymysql.connect(host='localhost', user=user, passwd=pswd, db='brain-arts', cursorclass=pymysql.cursors.DictCursor)
	cursor = connection.cursor()
	# query for event listings
	query = 'SELECT event_name, event_venue, event_time FROM event_listings ORDER BY event_time LIMIT 10;'
	cursor.execute(query)
	events = cursor.fetchall()
	# write event listings to template
	with open(html_template, 'w') as out
		for event in events:
			# TODO: write to html template
			out.write(event['event_name'])
			out.write(event['event_venue'])
