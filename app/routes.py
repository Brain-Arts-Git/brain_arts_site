from flask import render_template
from app import app


@app.route('/')
@app.route('/home')
def home():
	shows = [
		{
			'artist': 'Bon Iver',
			'location': 'TD Garden',
			'date': '11/20/19'
		},
		{
			'artist': '''Margot and the Nuclear So and So's''',
			'location': 'TD Garden',
			'date': '11/25/29'
		}
	]
	return render_template('home.html', shows=shows) #add arguments here
