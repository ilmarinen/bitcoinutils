from tracker import db
from flask_sqlalchemy import orm
from flask_login import UserMixin
from tracker import login
from tracker.lib import crypto


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    blocked = db.Column(db.Boolean, default=False)
    profile_filename = db.Column(db.String(70))
    external_auth = db.Column(db.String(20))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password_string):
        if password_string:
            self.password_hash = crypto.hash_pass(password_string)
        else:
            self.password_hash = None

    def verify_password(self, password):
        return crypto.verify_pass(password, self.password_hash)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Group {}>'.format(self.username)


class Membership(db.Model):
    __tablename__ = "memberships"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

    user = orm.relationship(User, backref=orm.backref("orders", cascade="all, delete-orphan"))
    group = orm.relationship(Group, backref=orm.backref("groups", cascade="all, delete-orphan"))


class Address(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(40), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    final_balance = db.Column(db.Integer)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(100), unique=True)


class AddressTransaction(db.Model):
    __tablename__ = "address_transactions"

    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    transaction_id = db.Column(db.Integer, db.ForeignKey("transactions.id"))

    address = orm.relationship(
        Address,
        backref=orm.backref("addresses", cascade="all, delete-orphan"))
    transaction = orm.relationship(
        Transaction,
        backref=orm.backref("transactions", cascade="all, delete-orphan"))

    @property
    def hash(self):
        return self.transaction.hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
