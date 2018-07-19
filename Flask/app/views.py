from flask import render_template

from app import app

@app.route('/')
def hello():
	hello = {
		'name': 'Flask framework'
	}
	
	return render_template('hello.html', hello=hello)