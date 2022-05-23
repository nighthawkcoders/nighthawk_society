from model import User
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required, login_manager, logout_user, login_user
from flask_restful import Api
import hashlib

app_crudu = Blueprint('usercrud', __name__,
                      url_prefix='/usercrud',
                      template_folder='templates/pages/',
                      static_folder='static',
                      static_url_path='assets')

@app_crudu.route('/')
# @login_required # login_url="/adminlogin/"
def crudu():
    """obtains all Users from table and loads Admin Form"""
    return render_template("crudu.html", table=users_all())

# SQLAlchemy extract all users from database
def users_all():
    table = User.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready

# SQLAlchemy extract users from database matching term
def users_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = User.query.order_by(User.name).filter((User.name.ilike(term)) | (User.email.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def user_by_id(userid):
    """finds User in table matching userid """
    return User.query.filter_by(id=userid).first()


# SQLAlchemy extract single user from database matching email
def user_by_email(email):
    """finds User in table matching email """
    return User.query.filter_by(email=email).first()


if __name__ == "__main__":
    # Look at table
    print("Print all")
    for user in users_all():
        print(user)
    print()

    # Look at table
    print("Print ilike example.com")
    for user in users_ilike("example.com"):
        print(user)
    print()

    print("Print user_id 2")
    print(user_by_id(2).read())

    print("Print user_id tedison@example.com")
    print(user_by_email("tedison@example.com").read())

