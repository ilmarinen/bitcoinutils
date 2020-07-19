import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = (os.environ.get("DATABASE_URL") or
        "sqlite:///{}".format(os.path.join(basedir, "tracker.db")))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = (os.environ.get("SECRET_KEY") or "secret-key")

    ADMIN = (os.environ.get("ADMIN") or "test@test.com")

    HOSTNAME = (os.environ.get("HOSTNAME") or "localhost:5000")

    UPLOAD_FOLDER = os.path.join(basedir, "../uploads")
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
