from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from os import urandom

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), unique=False, nullable=True)

    first_name = db.Column(db.String(255), nullable=True)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)

    avatar_uri = db.Column(db.String(512), default='empty.jpg', nullable=False)

    contacts = db.Column(db.String(512), nullable=True)

    vk_id = db.Column(db.String(255), nullable=True)
    vkaccesstoken = db.Column(db.String(512), nullable=True)
    fb_id = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True)

    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)

    thesesthemes = db.relationship("ThesesThemes", backref=db.backref("author", uselist=False), foreign_keys = 'ThesesThemes.author_id')

    def get_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __repr__(self):
        return f"{self.last_name}, {self.first_name}, {self.middle_name}"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title= db.Column(db.String(255), default='', nullable=False)
    logo = db.Column(db.String(255), default='empty.png', nullable=False)

class ThesesThemes(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title_ru = db.Column(db.String(255), default='', nullable=False)
    description = db.Column(db.String(1024), default='', nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), default=1, nullable=True)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    publish_year = db.Column(db.Integer, default=2021, nullable=False)

    requirements = db.Column(db.String(512), nullable=True)

class Level(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default='', nullable=False)

def init_db():

    users = [
        {'email' : 'ilya@hackerdom.ru', 'last_name' : 'Зеленчук', 'first_name' : 'Илья',
         'avatar_uri' : 'zelenchuk.jpg'}
        ]

    # Init DB
    db.session.commit() # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()

    # Create users
    print ("Create users")
    for user in users:
        u = Users(email=user['email'], password_hash = generate_password_hash(urandom(16).hex()),
                  first_name = user['first_name'], last_name = user['last_name'],
                  avatar_uri = user['avatar_uri'])

        db.session.add(u)
        db.session.commit()