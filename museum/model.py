from __init__ import db, app, admin, login
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, UserMixin
from flask_admin.contrib.sqla import ModelView
from flask import render_template, request, url_for, redirect
import hashlib


'''
Objective: Database Model to support students creating Projects, ultimately for showcasing at N@tM
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- i.  ) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
# -- ii. ) db.Model is like an inner layer of the onion of the ORM
# -- iii.) class Project, Job, User represents data to store in database, a table, something that is built on db.Model
## --iv .) relationship patters allow each table to work with or associate with other tables

Resources:
This page seems well maintained and has many videos
https://www.sqlalchemy.org/library.html#tutorials

This model.py is using advanced relationship patterns as described in the reference:  
https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html

This video is 7 minutes and shares a lot of more advanced relationship concepts
https://www.youtube.com/watch?v=47i-jzrrIGQ

'''

# Define a many-to-many association table
# ... used as table in the middle between Project and Tag, see ForeignKeys
projects_tags = db.Table('projects_tags',
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                         )


# Define a many-to-many association table with extra data
# ... used as table in the middle between Project and Job, see ForeignKeys
# ... defined as Class as ProjectJob contains user_id, which is assigned in code
class ProjectJob(db.Model):
    __tablename__ = 'projects_jobs'

    project_id = db.Column(db.ForeignKey('projects.id'), primary_key=True)
    job_id = db.Column(db.ForeignKey('jobs.id'), primary_key=True)
    user_id = db.Column(db.Integer)  # "extra data" in association, a user_id associated with a ProjectJob
#     project is associated with job, and in the relation there is a user

# Define the notes table
# ... objective of Note is to allow Project viewer write/blog notes on the project
# ... each Note belongs to one project, see ForeignKeys
class Note(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to id of who originates the note, many-to-one (many notes for each project)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, note, user_id):
        self.note = note
        self.id = user_id

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.project_id) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "project_id": self.project_id
        }


# Define the users table within the model
# ... objective of User is store an individual record of student, teacher, etc
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # define the Users schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, email="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(email) > 0:
            self.email = email
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented user.id
    def get_id(self):
        return self.id

    def get_rows(self):
        return db.session.query(self).count()



# Define the projects table
# ... objective of Project is store an key content related to student/scrum team project
class Project(db.Model):
    __tablename__ = 'projects'

    # Define the Projects schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    scrum_team = db.Column(db.String(255))
    description = db.Column(db.Text)
    jobs = db.relationship('Job', secondary='projects_jobs', back_populates='projects')
    tags = db.relationship('Tag', secondary='projects_tags', back_populates='projects')
    github_link = db.Column(db.String(255), unique=False, nullable=False)
    pages_link = db.Column(db.String(255), unique=False, nullable=False)
    video_link = db.Column(db.String(255), unique=False, nullable=False)
    run_link = db.Column(db.String(255), unique=False, nullable=False)
    notes = db.relationship(Note, cascade='all, delete', backref='projects', lazy=True)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, scrum_team, description, github_link, pages_link, video_link, run_link, password):
        self.name = name
        self.scrum_team = scrum_team
        self.description = description
        self.github_link = github_link
        self.pages_link = pages_link
        self.video_link = video_link
        self.run_link = run_link
        self.set_password(password)

    def create(self):
            try:
                db.session.add(self)
                db.session.commit()
                return self
            except IntegrityError:
                db.session.remove()
                return None

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "scrum_team": self.scrum_team,
            "description": self.description,
            "jobs": self.jobs,
            "tags": self.tags,
            "github_link": self.github_link,
            "pages_link": self.pages_link,
            "video_link": self.video_link,
            "run_link": self.run_link,
            "notes": self.notes,
            "password": self.password
        }

    def update(self, name="", scrum_team="", description="", github_link="", pages_link="", video_link="", run_link="", password=""):
        if len(name) > 0:
            self.name = name
        if len(scrum_team) > 0:
            self.scrum_team = scrum_team
        if len(description) > 0:
            self.description = description
        if len(github_link) > 0:
            self.github_link = github_link
        if len(pages_link) > 0:
            self.pages_link = pages_link
        if len(video_link) > 0:
            self.video_link = video_link
        if len(run_link) > 0:
            self.run_link = run_link
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

        # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result


# Define the jobs table
# ... objective of Job is define key jobs within the project
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_jobs', back_populates='jobs')

    def __init__(self, name):
        self.name = name

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
        }

# Define the tags table
# ... objective of Tag is define key attributes, aka #hashtag, used within the project
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_tags', back_populates='tags')


# This table contains the admin password. The encrypted version is stored.
class Passwords(db.Model, UserMixin):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.set_password(password)

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "name": self.name,
            "password": self.password,
        }


    def update(self, name="", password=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

 
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    def get_id(self):
        return (self.ID)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

"""Database Creation and Testing section"""


# General purpose add and commit method
# ... commit data to table
def model_adder(table):
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print("Records exist: duplicate key, or other error")


# General purpose table visualizer
# ... print schema and data within table
def model_printer(command):
    print("------------")
    print("Table: " + command)
    print("------------")
    result = db.session.execute(command)
    print(result.keys())
    for row in result:
        print(row)


# Hard Coded test data generator
# ... initial table creation with seed data
def model_init():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    table = [
        User(name='Thomas Edison', email='tedison@example.com', password='123toby'),
        User(name='Nicholas Tesla', email='ntesla@example.com', password='123niko'),
        User(name='Alexander Graham Bell', email='agbell@example.com', password='123lex'),
        User(name='Eli Whitney', email='eliw@example.com', password='123whit'),
        User(name='Marie Curie', email='marie@example.com', password='123marie'),
        User(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty'),
        User(name='Wilma Flintstone', email='wilma@example.com', password='123qwerty'),
        User(name='Betty Ruble', email='betty@example.com', password='123qwerty'),
        User(name='Fred Flintstone', email='fred@example.com', password='123qwerty'),
        User(name='Barney Ruble', email='barney@example.com', password='123qwerty'),
        User(name='Admin', email='Admin@Admin.com', password='Admin123'),

        Job(name="Scrum Master"),
        Job(name="GitHub Admin"),
        Job(name="Deployment Manager"),
        Job(name="Web Designer"),
        Job(name="Backend Developer"),

        Tag(name="Python"),
        Tag(name="Flask"),
        Tag(name="JavaScript"),
        Tag(name="SQL"),
        Tag(name="API"),
        Tag(name="Java"),
        Tag(name="Spring"),

        Project(name="Area 51",
                scrum_team="Aliens",
                description="Establish project database of aliens and their relations",
                github_link="https://github.com/nighthawkcoders",
                pages_link="https://nighthawkcoders.github.io/pages_python",
                video_link="https://nighthawkcoders.github.io/pages_python/comments",
                run_link="https://nighthawkcodingsociety.com/",
                password="1234"
                ),
        Project(name="Flintstones",
                scrum_team="Prehistoric Civilization",
                description="Establish project database of the Flintstones ancestors",
                github_link="https://github.com/nighthawkcoders",
                pages_link="https://nighthawkcoders.github.io/pages_java/",
                video_link="https://nighthawkcoders.github.io/pages_java/review",
                run_link="https://csa.nighthawkcodingsociety.com/",
                password="123456"
                ),
    ]
    model_adder(table)


# Hard Coded test data generator
# ... initial table creation with seed data
def model_relations_print(projects):
    for project in projects:
        print()
        print("ID:", project.id, " Name:", project.name, " Scrum Team:", project.scrum_team)
        print("Description:", project.description)
        print("GitHub Link:", project.github_link)
        print("GitHub Pages:", project.pages_link)
        print("Runtime Link:", project.run_link)
        print("Commercial Video:", project.video_link)
        for job in project.jobs:
            assoc = ProjectJob.query.filter_by(project_id=project.id).filter_by(job_id=job.id).first()
            usr = User.query.filter_by(id=assoc.user_id).first()
            print("\tEngineer:", job.id, job.name + ",", usr.name)
        for tag in project.tags:
            print("\tTag:", tag.name)


# Hard Coded relation data generator
# ... adding initial relationship data
def model_relations():
    # Project test data
    area51 = Project.query.filter_by(name="Area 51").first()
    stones = Project.query.filter_by(name="Flintstones").first()

    # Job test data
    scrum = Job.query.filter_by(name="Scrum Master").first()
    git = Job.query.filter_by(name="GitHub Admin").first()
    deploy = Job.query.filter_by(name="Deployment Manager").first()
    web = Job.query.filter_by(name="Web Designer").first()
    be = Job.query.filter_by(name="Backend Developer").first()

    # Tag test data (like a #hashtag)
    python = Tag.query.filter_by(name="Python").first()
    flask = Tag.query.filter_by(name="Flask").first()
    js = Tag.query.filter_by(name="JavaScript").first()
    java = Tag.query.filter_by(name="Java").first()
    spring = Tag.query.filter_by(name="Spring").first()

    # Area51 build relations between Project, Jobs, and Users
    # Scrum Team User
    area51.jobs.append(scrum)
    assoc = ProjectJob.query.filter_by(project_id=area51.id).filter_by(job_id=scrum.id).first()
    usr = User.query.filter_by(email="ntesla@example.com").first()
    assoc.user_id = usr.id
    # Git Hub User
    area51.jobs.append(git)
    assoc = ProjectJob.query.filter_by(project_id=area51.id).filter_by(job_id=git.id).first()
    usr = User.query.filter_by(email="marie@example.com").first()
    assoc.user_id = usr.id
    # Deployment User
    area51.jobs.append(deploy)
    assoc = ProjectJob.query.filter_by(project_id=area51.id).filter_by(job_id=deploy.id).first()
    usr = User.query.filter_by(email="tedison@example.com").first()
    assoc.user_id = usr.id
    # Web Designer User
    area51.jobs.append(web)
    assoc = ProjectJob.query.filter_by(project_id=area51.id).filter_by(job_id=web.id).first()
    usr = User.query.filter_by(email="agbell@example.com").first()
    assoc.user_id = usr.id
    # Backend Developer
    area51.jobs.append(be)
    assoc = ProjectJob.query.filter_by(project_id=area51.id).filter_by(job_id=be.id).first()
    usr = User.query.filter_by(email="eliw@example.com").first()
    assoc.user_id = usr.id
    # Tag Data: build relations between Project and Tag data
    area51.tags.append(python)
    area51.tags.append(flask)
    area51.tags.append(js)

    # Flintstones data build relations between Project, Jobs, and Users
    stones.jobs.append(scrum)
    assoc = ProjectJob.query.filter_by(project_id=stones.id).filter_by(job_id=scrum.id).first()
    usr = User.query.filter_by(email="jmort1021@gmail.com").first()
    assoc.user_id = usr.id
    stones.jobs.append(git)
    assoc = ProjectJob.query.filter_by(project_id=stones.id).filter_by(job_id=git.id).first()
    usr = User.query.filter_by(email="barney@example.com").first()
    assoc.user_id = usr.id
    stones.jobs.append(deploy)
    assoc = ProjectJob.query.filter_by(project_id=stones.id).filter_by(job_id=deploy.id).first()
    usr = User.query.filter_by(email="betty@example.com").first()
    assoc.user_id = usr.id
    stones.jobs.append(web)
    assoc = ProjectJob.query.filter_by(project_id=stones.id).filter_by(job_id=web.id).first()
    usr = User.query.filter_by(email="wilma@example.com").first()
    assoc.user_id = usr.id
    stones.jobs.append(be)
    assoc = ProjectJob.query.filter_by(project_id=stones.id).filter_by(job_id=be.id).first()
    usr = User.query.filter_by(email="fred@example.com").first()
    assoc.user_id = usr.id
    stones.tags.append(java)
    stones.tags.append(spring)
    stones.tags.append(js)

    # commit data
    db.session.commit()

    return [area51, stones]


# Function that automates creating associations between users and projects.
def createAssociation(projectID, userID, jobID):
    # Getting the project, user, and job object from the inputted ID's
    project = Project.query.filter_by(id = projectID).first()
    user = User.query.filter_by(id = userID).first()
    job = Job.query.filter_by(id = jobID).first()
    # Checking if there is already an association between the job and the project. If one already exists, then the user is updated to the inputted one.
    if job not in project.jobs:
        # If there is not an association, then it is created, and assigned the inputted user.
        project.jobs.append(job)
    assoc = ProjectJob.query.filter_by(project_id=project.id).filter_by(job_id=job.id).first()
    assoc.user_id = user.id
    db.session.commit()

    projects = [project]
    model_relations_print(projects)

def passwords_model_tester():
    print("--------------------------")
    print("Seed Data for Table: Passwords")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    t1 = Passwords(name='Admin', password='jmort123')
    table = [t1]
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            print("error")
            db.session.remove()

def passwords_model_printer():
    print("------------")
    print("Table: passwords with SQL query")
    print("------------")
    result = db.session.execute('select * from passwords')
    print(result.keys())
    for row in result:
        print(row)

# print tables
# ... send to model_printer select commands for all tables generated by this project
def model_print():
    model_printer('select * from users')
    model_printer('select * from jobs')
    model_printer('select * from tags')
    model_printer('select * from projects')
    model_printer('select * from projects_jobs')
    model_printer('select * from projects_tags')


# tester/driver
# ... driver calls init (db_create_all) which establishes database with tables and seeds content
# ... driver calls model_relations which completes seed by establishing sample data relations
# ... driver call two print methods to allow user to visualize success
if __name__ == "__main__":
    model_init()  # builds model of Users
    projects = model_relations()
    model_print()
    model_relations_print(projects)
    passwords_model_tester()  # builds model of Passwords
    passwords_model_printer()

def encryption(code):
    encrypted = hashlib.sha256(code.encode()).hexdigest()
    return encrypted


# Userloader for login
@login.user_loader
def load_user(userID):
    return User.query.get(userID)

# This creates the admin database page
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

# Admin login, called in authorize.
@app.route('/adminlogin/', methods=['GET', 'POST'])
def login():
    if request.form:
        adminpass = request.form.get("adminpass")
        pw = Passwords.query.filter(Passwords.name == "Admin").first()
        if (pw.is_password_match(adminpass)):
            user = User.query.filter(User.name == "Admin").first()
            login_user(user)
            return redirect('/admin/')# where is the render template??? LMFAO
        else:
            print("no")
    return render_template("authorize.html")


# Defining the tables that the admin sees on the admin database.
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Project, db.session))
admin.add_view(MyModelView(Passwords, db.session))

