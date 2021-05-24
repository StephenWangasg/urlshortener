from flask import (
    Blueprint,  redirect, render_template, request
)
from werkzeug.exceptions import abort
from db.dbmanager import DBManager

dbmanager = DBManager()

bp = Blueprint('url', __name__)

@bp.route('/')
def index():
    links = dbmanager.getall()

    return render_template('url/index.html', links=links)

@bp.route('/url/shorten', methods=('GET', 'POST'))
def shorten():
    link = None

    if request.method == 'POST':
        long_url = request.form['long_url']

        link = dbmanager.get(long_url)

        if link is None:
            link = dbmanager.add(long_url)
            
    return render_template('url/shorten.html', link=link)

@bp.route('/<short_code>')
def unshorten(short_code):
    
    print("Unshortening {}".format(short_code))
    link = dbmanager.find(short_code)

    if link is not None:
        return redirect(link.long_url)

    abort(404)
