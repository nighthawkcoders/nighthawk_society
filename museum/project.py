from model import User
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
                po.update(name, email, password)
    return redirect(url_for('usercrud.crudu'))

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
    print(project_by_email("tedison@example.com").read())

