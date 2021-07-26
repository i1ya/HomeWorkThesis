# -*- coding: utf-8 -*-
import sys, os
from flask import Flask, render_template
from sqlalchemy.sql.expression import func

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lk.html')
def lk():
    user = Users.query.filter_by(id=1).first()

    return render_template('lk.html', user=user)

if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
        init_db()
    else:
        app.run(port=5000)