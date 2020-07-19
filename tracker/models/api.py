from tracker import db
from tracker.models import models
from flask_login import login_user
from tracker.lib.http import APIException


def set_user_password(user, password):
    user.password = password
    db.session.add(user)
    db.session.commit()


def get_user_by_email(email):
    user = models.User.query.filter_by(email=email).first()
    return user


def get_user_by_username(username):
    user = models.User.query.filter_by(username=username).first()
    return user


def check_email_exists(email):
    users = models.User.query.filter_by(email=email).all()
    return (len(users) > 0)


def create_user(username, firstname, lastname, email, profile_filename=None,
                external_auth="", is_active=False, restaurant_owner=False,
                password=None):
    user = models.User(
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        profile_filename=profile_filename,
        external_auth=external_auth,
        is_active=is_active)
    if password is not None:
        user.password = password
    db.session.add(user)
    db.session.flush()

    if restaurant_owner:
        restaurant_owner_group = models.Group.query.filter_by(
            groupname="restaurant_owners").first()
        membership = models.Membership(
            user_id=user.id, group_id=restaurant_owner_group.id)
        db.session.add(membership)
        db.session.flush()

    db.session.commit()
    return user


def update_user(user_id, firstname, lastname):
    user = models.User.query.get(user_id)
    if user is None:
        raise APIException(404, "Not found.")
    user.firstname = firstname
    user.lastname = lastname
    db.session.add(user)
    db.session.commit()
    return user


def block_user_by_username(username):
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        raise APIException(404, "Not found.")
    user.blocked = True
    db.session.add(user)
    db.session.commit()
    return user


def unblock_user(user_id):
    user = models.User.query.get(user_id)
    if user is None:
        raise APIException(404, "Not found.")
    user.blocked = False
    user.failed_login_attempts = 0
    db.session.add(user)
    db.session.commit()
    return user


def failed_login(user):
    if user is not None:
        user.failed_login_attempts = user.failed_login_attempts + 1

    if user.failed_login_attempts == 3:
        user.blocked = True

    db.session.add(user)
    db.session.commit()


def authenticate(username, password):
    user = models.User.query.filter_by(username=username).first()
    if user.blocked:
        return False

    if user.verify_password(password) and user.blocked is False:
        user.failed_login_attempts = 0
        db.session.add(user)
        db.session.commit()
        return login_user(user)

    elif not user.verify_password(password):
        failed_login(user)

    return False
