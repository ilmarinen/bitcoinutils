import os
from blockchain import util

from datetime import datetime
from flask import Flask, request, send_from_directory, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from tracker.config import Config
from tracker.lib.http import APIException


util.TIMEOUT = 300

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from tracker.models import models
from tracker.blueprints import users

basedir = os.path.abspath(os.path.dirname(__file__))

app.register_blueprint(users.rest_bp, url_prefix='/api')

admin = Admin(app, name="tracker", template_mode="bootstrap3")
admin.add_view(ModelView(models.User, db.session))


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(basedir, '/static'), path)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(basedir, 'static'), 'favicon.ico')


@login_required
@app.route('/uploads', methods=["POST"])
def uploads():
    if "file" not in request.files:
        raise APIException(403, "No files")
    file = request.files["file"]
    if file.filename == "":
        raise APIException(403, "No files selected")

    filename = "{}-{}.jpg".format(current_user.username, str(datetime.utcnow().timestamp()))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    current_user.profile_filename = filename
    db.session.add(current_user)
    db.session.commit()

    return "uploads/{}".format(filename)


@login_required
@app.route('/uploads/<path:path>')
def get_uploads(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', selected_tab="LOGIN")


@app.route('/signup')
def user_signup():
    return render_template('index.html', selected_tab="SIGNUP")


def gen_fixtures():
    from tracker.models import api

    admin_groups = models.Group.query.filter_by(groupname="admins")

    if admin_groups.count() == 0:
        admins = models.Group(groupname="admins")
        admin_user = models.User(username="admin")
        admin_user.password = "admin"
        admin_user.is_active = True
        db.session.add(admins)
        db.session.add(admin_user)
        db.session.flush()
        admins_membership = models.Membership(user_id=admin_user.id, group_id=admins.id)
        db.session.add(admins_membership)
        db.session.commit()

    user_a = api.create_user("jack", "Jack", "EinstSpratein", "t@test.com", is_active=True, password="test")
    user_b = api.create_user("john", "John", "Doe", "j@test.com", is_active=True, password="test")
    db.session.add(user_a)
    db.session.add(user_b)
    db.session.commit()


@app.cli.command("generate-fixtures")
def generate_fixtures():
    gen_fixtures()
