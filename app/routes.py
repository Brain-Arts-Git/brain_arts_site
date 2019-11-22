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
    """
    shows = []
    return render_template('home.html', shows=shows) #add arguments here

@app.route('/blog')
def blog():
    blogs = [
        {
            'title': 'Blog post 1',
            'date': 'November 21, 2019',
            'text': """
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                    \n
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
                    """
        }
    ]
    return render_template('blog.html', blogs=blogs)

@app.route('/admin')
def admin():
    return render_template('admin.html')