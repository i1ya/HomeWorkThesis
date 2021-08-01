from flask import Flask, render_template, redirect, url_for, abort
from flask import make_response, session, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import SQLAlchemyError
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
from pip._vendor import cachecontrol

import requests
import json
import sys, os
import pathlib

from models import db, init_db, Users, ThesesThemes, Level

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

# Flask configs
app.config['APPLICATION_ROOT'] = '/'

# SQLAlchimy config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///theseswork.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16).hex()

# Init Database
db.app = app
db.init_app(app)


@app.route('/lk.html')
def lk():
    user = Users.query.filter_by(id=1).first()
    return render_template('lk.html', user=user)


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('addThemes.html')


@app.route('/addThemes', methods=['GET', 'POST'])
def adding_themes():
    if request.method == 'POST':
        try:
            # user = Users.query.filter_by(id=1).first()
            title = request.form['name']
            desc = request.form['desc']
            wishes = request.form['wishes']
            techs = request.form['techs']
            new_theme = ThesesThemes(title_ru=title, description=desc,techs = techs,
                                     requirements=wishes)
            db.session.add(new_theme)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            print(error)
            print("Ошибка при добавлении темы в БД")
            return redirect(url_for('start'))
        # return render_template('addThemes.html')
        return redirect((url_for('lk')))
    else:
        return "<h1> Ошибка при добавлении темы в БД </h1>"


if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
        init_db()
    else:
        app.run(port=5000, debug="True")
