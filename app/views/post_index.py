from flask import render_template
from app import app
from dbfpy import dbf

@app.route('/refs/post_index_ref')
def post_index():
    return render_template('post_index.html')
