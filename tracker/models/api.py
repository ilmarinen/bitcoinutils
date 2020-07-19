from blockchain import blockexplorer
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


def add_address_transaction(address, blockchain_transaction):
    transaction = models.Transaction.query.filter_by(hash=blockchain_transaction.hash).first()
    if transaction is None:
        transaction = models.Transaction(hash=blockchain_transaction.hash)
        db.session.add(transaction)
        db.session.flush()

    address_transaction = models.AddressTransaction.query.filter_by(
        address_id=address.id, transaction_id=transaction.id).first()
    if address_transaction is None:
        address_transaction = models.AddressTransaction(address_id=address.id, transaction_id=transaction.id)
        db.session.add(address_transaction)
        db.session.flush()
        db.session.commit()

    return address_transaction


def get_or_create_address(user_id, address_string):
    user = models.User.query.get(user_id)
    if user is None:
        raise APIException(404, "Not found.")

    address = models.Address.query.filter_by(address=address_string).first()
    if address is None:
        blockchain_address = blockexplorer.get_address(address_string)
        address = models.Address(
            address=address_string,
            user_id=user.id,
            final_balance=blockchain_address.final_balance)
        db.session.add(address)
        db.session.commit()
        for blockchain_transaction in blockchain_address.transactions:
            add_address_transaction(address, blockchain_transaction)

    return address


def get_user_addresses(user_id):
    addresses = models.Address.query.filter_by(user_id=user_id).all()
    return addresses


def get_user_address(user_id, address_id):
    address = models.Address.query.filter_by(user_id=user_id, id=address_id).first()
    return address


def update_user_address(user_id, address_id):
    address = get_user_address(user_id, address_id)
    blockchain_address = blockexplorer.get_address(address.address)
    address.final_balance = blockchain_address.final_balance
    db.session.add(address)
    db.session.commit()
    for blockchain_transaction in blockchain_address.transactions:
        add_address_transaction(address, blockchain_transaction)

    return address


def get_user_address_transactions(user_id, address_id):
    address = get_user_address(user_id, address_id)
    address_transactions = models.AddressTransaction.query.filter_by(address_id=address.id).all()
    return address_transactions


def get_address_transaction(address_transaction_id):
    address_transactions = models.AddressTransaction.query.filter_by(id=address_transaction_id).all()
    return address_transactions
