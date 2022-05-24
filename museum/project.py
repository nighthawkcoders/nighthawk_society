from model import User, Project
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_login import login_required, login_manager, logout_user, login_user
from flask_restful import Api
import hashlib

app_project = Blueprint('project', __name__,
                      url_prefix='/project',
                      template_folder='museum/',
                      static_folder='static',
                      static_url_path='assets')

# SQLAlchemy extract all users from database
def project_all():
    table = Project.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready

# SQLAlchemy extract users from database matching term
def project_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Project.query.order_by(Project.name).filter((Project.name.ilike(term)) | (Project.scrum_team.ilike(term)) | (Project.description.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def project_by_id(projectid):
    """finds User in table matching userid """
    return Project.query.filter_by(id=projectid).first()


# SQLAlchemy extract single user from database matching email
def project_by_name(name):
    """finds User in table matching email """
    return User.query.filter_by(name=name).first()

def project_by_scrum_name(scrum_name):
    """finds User in table matching email """
    return User.query.filter_by(scrum_name=scrum_name).first()

def project_by_description(description):
    """finds User in table matching email """
    return User.query.filter_by(description=description).first()


# @login_manager.project_loader
# def project_loader(projectid):
#     """Check if user login status on each page protected by @login_required."""
#     if projectid is not None:
#         return Project.query.get(projectid)
#     return None
