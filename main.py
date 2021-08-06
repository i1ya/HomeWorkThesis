# -*- coding: utf-8 -*-
import sys, os
from flask import Flask, render_template, request
from sqlalchemy.sql.expression import func

from models import db, init_db, Users, ThesesThemes, Level, Department

from filter_form import ThesisFilter

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

@app.route('/listofthemes.html')
def theses_search():
    filter = ThesisFilter()
    filter.levels.choices = [(levels.id, levels.title) for levels in Level.query.all()]
    filter.department.choices = [(dp.id, dp.title) for dp in Department.query.all()]

    for sid in ThesesThemes.query.with_entities(ThesesThemes.supervisor_id).distinct().all():
        user = Users.query.filter_by(id=sid[0]).first()
        last_name = ""
        initials = ""

        if user.last_name:
            last_name = user.last_name

        if user.first_name:
            initials = initials + user.first_name[0] + "."

        if user.middle_name:
            initials = initials + user.middle_name[0] + "."

        filter.supervisor.choices.append((sid[0], last_name + " " + initials))
        filter.supervisor.choices.sort(key=lambda tup: tup[1])

        filter.supervisor.choices.insert(0, (0, "Все"))


    return render_template('listofthemes.html', filter=filter)

@app.route('/fetch_themes')
def fetch_themes():

    levels = request.args.get('levels', default=1, type=int)
    page = request.args.get('page', default=1, type=int)
    supervisor = request.args.get('supervisor', default=0, type=int)
    department = request.args.get('department', default=0, type=int)

    records = ThesesThemes.query.order_by(ThesesThemes.id.desc())

    if supervisor:

        # Check if supervisor exists
        ids = ThesesThemes.query.with_entities(ThesesThemes.supervisor_id).distinct().all()
        if [item for item in ids if item[0] == supervisor]:
            records = records.filter(ThesesThemes.supervisor_id == supervisor)
        else:
            supervisor = 0

    if department:

        # Check if department exists
        idis = ThesesThemes.query.with_entities(ThesesThemes.advisor_id).distinct().all()
        if [item for item in idis if item[0] == department]:
            records = records.filter(ThesesThemes.advisor_id == department)
        else:
            department = 0

    if levels > 1:
        records = records.filter_by(level_id=levels).paginate(per_page=10, page=page, error_out=False)
    else:
        records = records.paginate(per_page=2, page=page, error_out=False)

    if len(records.items):
        return render_template('fetch_themes.html', themes=records, levels=levels, supervisor=supervisor, department=department)
    else:
        return render_template('fetch_themes_blank.html')


if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
        init_db()
    else:
        app.run(port=5000)