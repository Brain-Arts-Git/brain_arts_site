from flask import render_template
from app import app


@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    """ 
    this should turn into a call to a function that reads a text file with the 
    shows and then returns them in the following list of dicts format, or just
    a call to a database. 
    """
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
