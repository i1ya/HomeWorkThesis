# -*- coding: utf-8 -*-
import sys, os
from flask import Flask, render_template, request, redirect
from sqlalchemy.sql.expression import func
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route('/edit-lk.html', methods=["POST", "GET"])
def edit_lk():
    statuses = ["Преподаватель кафедры СП", ]
    user = Users.query.filter_by(id=1).first()
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.middle_name = request.form['middle_name']
        user.last_name = request.form['last_name']

        password = request.form['password']
        password_check = request.form['password_check']
        if password == password_check:
            user.password_hash = generate_password_hash(password)
        else:
            return "Пароли не совпадают!"

        try:
            db.session.commit()
            return redirect("/lk.html")
        except:
            return "Ошибка сохранения"
    else:
        return render_template('edit_lk.html', user=user)


if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
        init_db()
    else:
        app.run(port=5000, debug=True)
