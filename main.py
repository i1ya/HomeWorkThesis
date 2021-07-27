# -*- coding: utf-8 -*-
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

login_manager = LoginManager()
login_manager.init_app(app)

# Google auth (https://github.com/code-specialist/flask_google_login/blob/main/app.py)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "593053078492-i6hf335m9hm0vtj23df62q09j07esbhu.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/google_callback"
)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/google_callback')
def google_callback():

    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    avatar_uri = os.urandom(16).hex()
    avatar_uri = avatar_uri + ".jpg"

    if 'picture' in id_info:
        r = requests.get(id_info.get('picture'), allow_redirects=True)
        open('static/assets/avatars/' + avatar_uri, 'wb').write(r.content)

    user = Users.query.filter_by(google_id=id_info.get('email')).first()

    # New user?
    if user is None:
        # Yes
        try:
            new_user = Users(last_name=id_info.get('family_name'),
                             first_name=id_info.get('given_name'),
                             avatar_uri=avatar_uri,
                             google_id=id_info.get('email'))
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            print(error)
            print("Ошибка при добавлении пользователя в БД")
            return redirect(url_for('index'))

        user = Users.query.filter_by(google_id=id_info.get('email')).first()

    login_user(user, remember=True)
    return redirect(url_for('lk'))

# https://vk.com/dev/authcode_flow_user
@app.route("/vk_callback")
def vk_callback():

    user_code = request.args.get('code')

    if not user_code:
        return redirect(url_for('index'))

    # Get access token
    response = requests.get('https://oauth.vk.com/access_token?client_id=7912054&client_secret=rIE4Ef9876ktwXHFrgyU&redirect_uri=http://127.0.0.1:5000/vk_callback&code=' + user_code)
    access_token_json = json.loads(response.text)

    if "error" in access_token_json:
        return redirect(url_for('index'))

    vk_id = access_token_json['user_id']
    access_token = access_token_json['access_token']

    # Get user name
    response = requests.get('https://api.vk.com/method/users.get?user_ids=' + str(vk_id) + '&fields=photo_100&access_token=' + str(access_token) + '&v=5.130')
    vk_user = json.loads(response.text)

    avatar_uri = os.urandom(16).hex()
    avatar_uri = avatar_uri + ".jpg"

    if 'photo_100' in vk_user['response'][0]:
        r = requests.get(vk_user['response'][0]['photo_100'], allow_redirects=True)
        open('static/assets/avatars/' + avatar_uri, 'wb').write(r.content)

    user = Users.query.filter_by(vk_id=vk_id).first()

    # New user?
    if user is None:
        # Yes
        try:
            new_user = Users(last_name=vk_user['response'][0]['last_name'],
                             first_name=vk_user['response'][0]['first_name'],
                             avatar_uri=avatar_uri,
                             vk_id=vk_id, vkaccesstoken=access_token)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            print(error)
            print("Ошибка при добавлении пользователя в БД")
            return redirect(url_for('index'))

        user = Users.query.filter_by(vk_id=vk_id).first()

    login_user(user, remember=True)
    return redirect(url_for('lk'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register-basic.html')
def register_basic():
    return render_template("register-basic.html")


@app.route('/password-recovery.html')
def password_recovery():
    return render_template("password-recovery.html")

@app.route('/lk.html')
@login_required
def lk():

    user = Users.query.filter_by(id=current_user.id).first()

    return render_template('lk.html', user=user)

if __name__ == '__main__':

    if (len(sys.argv) > 1) and (sys.argv[1] == "init"):
        init_db()
    else:
        app.run(port=5000)