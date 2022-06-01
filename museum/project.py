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


@app_project.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = Project(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
        )
        po.create()
    return redirect(url_for('project.project'))

# CRUD update
@app_project.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        id = request.form.get("userID")
        pname = request.form.get("pname")
        scrum_team = request.form.get("scrum")
        description = request.form.get("email")
        github_link = request.form.get("git")
        pages_link = request.form.get("pages")
        video_link = request.form.get("vid")
        run_link = request.form.get("run")
        password = request.form.get("password")
        print(id)
        print(pname)
        print(scrum_team)
        print(description)
        print(github_link)
        print(pages_link)
        print(video_link)
        print(run_link)
    po = project_by_id(id)
    if po is not None:
        if (po.is_password_match(password)):
            po.update(pname, scrum_team, description, github_link, pages_link, video_link, run_link, password)
    return redirect(url_for('project.project'))


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


# @login.project_loader
# def project_loader(projectid):
#     """Check if user login status on each page protected by @login_required."""
#     if projectid is not None:
#         return Project.query.get(projectid)
#     return None


if __name__ == "__main__":
    # Look at table
    print("Print all")
    for user in project_all():
        print(user)
    print()

    # Look at table
    print("Print ilike example.com")
    for user in project_ilike("example.com"):
        print(user)
    print()

    print("Print user_id 2")
    print(project_by_id(2).read())

    print("Print user_id tedison@example.com")
    print(project_by_scrum_name("tedison@example.com").read())