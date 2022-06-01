from __init__ import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_manager, logout_user, login_user
from museum.model import User, Project, Job, ProjectJob, createAssociation, Passwords
from flask import Blueprint, render_template, request, url_for, redirect, jsonify, make_response
from flask_restful import Api
import hashlib

app_crudu = Blueprint('usercrud', __name__,
                      url_prefix='/usercrud',
                      template_folder='templates/pages/',
                      static_folder='static',
                      static_url_path='assets')


@app_crudu.route('/')
def crudu():
    return render_template("crudu.html", table=users_all())

@app_crudu.route('/projects/')
def findproject():
    return render_template("findproject.html", users=users_all(), projects=projects_all(), jobs=jobs_all())

@app_crudu.route('/viewproject/')
def viewProject():
    return render_template("viewProject.html", projects=projects_all(),
                           id="", name="",team="",description="",
                           jobs="", users="", tags="")
# SQLAlchemy extract all users from database
def users_all():
    table = User.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


def projects_all():
    table = Project.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready

def jobs_all():
    table = Job.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# SQLAlchemy extract users from database matching term
def users_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = User.query.order_by(User.name).filter((User.name.ilike(term)) | (User.email.ilike(term)))
    return [peep.read() for peep in table]

def projects_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    x = Project.query.order_by(Project.name).filter((Project.name.ilike(term))).first()
    return x

# SQLAlchemy extract single user from database matching ID
def user_by_id(userid):
    """finds User in table matching userid """
    return User.query.filter_by(id=userid).first()

def project_by_id(projectID):
    """finds User in table matching userid """
    return Project.query.filter_by(id=projectID).first()


# SQLAlchemy extract single user from database matching email
def user_by_email(email):
    """finds User in table matching email """
    return User.query.filter_by(email=email).first()


@login.user_loader
def user_loader(id):
    """Check if user login status on each page protected by @login_required."""
    if id is not None:
        return User.query.get(id)
    return None

@app_crudu.route('/create/', methods=["POST"])
def create():
    """gets data from form and add it to Users table"""
    if request.form:
        po = User(
            request.form.get("name"),
            request.form.get("email"),
            request.form.get("password"),
        )
        po.create()
    return redirect(url_for('usercrud.crudu'))

# CRUD update
@app_crudu.route('/update/', methods=["POST"])
def update():
    """gets userid and name from form and filters and then data in  Users table"""
    if request.form:
        id = request.form.get("userID")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(id)
        print(name)
        print(email)
        print(password)
        po = user_by_id(id)
        if po is not None:
            if (po.is_password_match(password)):
                po.update(name, email, password)
    return redirect(url_for('usercrud.crudu'))


@app_crudu.route('/updateProject/', methods=["POST"])
def updateProject():
    if request.form:
        projectID = request.form.get("projectID")
        userID = request.form.get("userID")
        jobID = request.form.get("jobID")
        password = request.form.get("pass")
        po = user_by_id(userID)
        if po is not None:
            if (po.is_password_match(password)):
                createAssociation(projectID, userID, jobID)
    return redirect(url_for('usercrud.findproject'))

@app_crudu.route('/updateProjectInfo/', methods=["POST"])
def updateProjectInfo():
    if request.form:
        id = request.form.get("projectID2")
        name = request.form.get("namep")
        scrum = request.form.get("scrum_teamp")
        description = request.form.get("descriptionp")
        glink = request.form.get("github_linkp")
        plink = request.form.get("pages_linkp")
        vlink = request.form.get("video_linkp")
        rlink = request.form.get("run_linkp")
        password = request.form.get("passwordp")
        po = project_by_id(id)
        if po is not None:
            if (po.is_password_match(password)):
                po.update(name, scrum, description, glink, plink, vlink, rlink, password)
    return redirect(url_for('usercrud.findproject'))

@app_crudu.route('/createProject/', methods=["POST"])
def createProject():
    if request.form:
        po = Project(
            request.form.get("name"),
            request.form.get("scrum_team"),
            request.form.get("description"),
            request.form.get("github_link"),
            request.form.get("pages_link"),
            request.form.get("video_link"),
            request.form.get("run_link"),
            request.form.get("passwordi")
        )
        po.create()
    return redirect(url_for('usercrud.findproject'))

@app_crudu.route('/view/', methods=["POST"])
def view():
    if request.form:
        # temp = request.form.get("projectName")
        projectID = request.form.get("projectID")
        project = Project.query.filter_by(id = projectID).first()
        # if temp is not None:
        #     if projects_ilike(temp) is not None:
        #         project = projects_ilike(temp)
        allusers=[]
        alljobs=[]
        for job in project.jobs:
            assoc = ProjectJob.query.filter_by(project_id=project.id).filter_by(job_id=job.id).first()
            usr = User.query.filter_by(id=assoc.user_id).first()
            allusers.append(usr.name)
            alljobs.append(job.name)
        # for tag in project.tags:
        #     print("\tTag:", tag.name)
    return render_template("viewProject.html", projects=projects_all(),
                           id=project.id, name=project.name,team=project.scrum_team, description=project.description,
                           jobs=alljobs, users=allusers, tags=project.tags, glink=project.github_link, plink=project.pages_link,vlink=project.video_link,
                           rlink=project.run_link)

@app_crudu.route('/adminlogout/')
def logout():
    logout_user()
    return redirect(url_for('usercrud.findproject'))

@app_crudu.route('/admin/')
def admin():
    return render_template("authorize.html")


@app_crudu.route('/reset/', methods=['GET', 'POST'])
@login_required
def reset():
    if request.form:
        adminpass = request.form.get("adminpass")
        pw = Passwords.query.filter(Passwords.name == "Admin").first()
        if (pw.is_password_match(adminpass)):
            newpass = request.form.get("newpass")
            pw.update("Admin", newpass)
            return redirect('/admin/')
        else:
            print("no")
    return render_template("reset.html")


def set_password(password):
    """Create hashed password."""
    password = generate_password_hash(password, method='sha256')
    return password



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

