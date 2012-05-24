from flask import render_template
from app import app

@app.route('/')
def root():
    return render_template('main.html')
