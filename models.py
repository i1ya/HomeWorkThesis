from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), unique=False, nullable=True)

    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)

    avatar_uri = db.Column(db.String(512), default='empty.jpg', nullable=False)

    contacts = db.Column(db.String(512), nullable=True)

    vk_id = db.Column(db.String(255), nullable=True)
    fb_id = db.Column(db.String(255), nullable=True)
    google_id = db.Column(db.String(255), nullable=True)

    department = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)

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
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), default=1, nullable=False)

    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    advisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    requirements = db.Column(db.String(512), nullable=True)

class Level(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), default='', nullable=False)

def init_db():

    # Init DB
    db.session.commit() # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()