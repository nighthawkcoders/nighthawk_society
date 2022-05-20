""" database dependencies to support Users db examples """
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along

# Define a many-to-many association table
projects_tags = db.Table('projects_tags',
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                         )


# Define a many-to-many association table with extra data
class ProjectJob(db.Model):
    __tablename__ = 'projects_jobs'

    project_id = db.Column(db.ForeignKey('projects.id'), primary_key=True)
    job_id = db.Column(db.ForeignKey('jobs.id'), primary_key=True)
    # This relations contains "extra data", a user_id associated with Job
    user_id = db.Column(db.Integer)


# Define the notes table
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
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # define the Users schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone

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
            "phone": self.phone,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        if len(phone) > 0:
            self.phone = phone
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
class Project(db.Model):
    __tablename__ = 'projects'

    # Define the Users schema
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


# Define the jobs table
class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_jobs', back_populates='jobs')


# Define the tags table
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_tags', back_populates='tags')


"""Database Creation and Testing section"""


# commit data to table
def model_adder(table):
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print("Records exist, duplicate email, or error")


# print data within table
def model_printer(command):
    print("------------")
    print("Table: " + command)
    print("------------")
    result = db.session.execute(command)
    print(result.keys())
    for row in result:
        print(row)


# table creation and initialization
def model_init():
    print("--------------------------")
    print("Seed Data for Table: users")
    print("--------------------------")
    db.create_all()
    """Tester data for table"""
    table = [
        User(name='Thomas Edison', email='tedison@example.com', password='123toby', phone="1111111111"),
        User(name='Nicholas Tesla', email='ntesla@example.com', password='123niko', phone="1111112222"),
        User(name='Alexander Graham Bell', email='agbell@example.com', password='123lex', phone="1111113333"),
        User(name='Eli Whitney', email='eliw@example.com', password='123whit', phone="1111114444"),
        User(name='Marie Curie', email='marie@example.com', password='123marie', phone="1111115555"),
        User(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty', phone="8587754956"),
        User(name='Wilma Flintstone', email='wilma@example.com', password='123qwerty', phone="0000001111"),
        User(name='Betty Ruble', email='betty@example.com', password='123qwerty', phone="0000001113"),
        User(name='Fred Flintstone', email='fred@example.com', password='123qwerty', phone="0000001112"),
        User(name='Barney Ruble', email='barney@example.com', password='123qwerty', phone="0000001114"),

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
                description="Establish project database aliens and relations",
                github_link="https://github.com/nighthawkcoders",
                pages_link="https://nighthawkcoders.github.io/pages_python",
                video_link="https://nighthawkcoders.github.io/pages_python/comments",
                run_link="https://nighthawkcodingsociety.com/",
                ),
        Project(name="Flintstones",
                scrum_team="Prehistoric Civilization",
                description="Establish project database Flintstones ancestors",
                github_link="https://github.com/nighthawkcoders",
                pages_link="https://nighthawkcoders.github.io/pages_java/",
                video_link="https://nighthawkcoders.github.io/pages_java/review",
                run_link="https://csa.nighthawkcodingsociety.com/",
                ),
    ]
    model_adder(table)


def model_relations_print(project):
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
        print("\tEngineer:", job.id, usr.name + ",", job.name)
    for tag in project.tags:
        print("\tTag:", tag.id, tag.name)


# adding and printing relationship data
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

    # print Jobs and Tags for Area 51
    model_relations_print(area51)
    # print Jobs and Tags for Flintstones
    model_relations_print(stones)


# print tables
def model_print():
    model_printer('select * from users')
    model_printer('select * from jobs')
    model_printer('select * from tags')
    model_printer('select * from projects')
    model_printer('select * from projects_jobs')
    model_printer('select * from projects_tags')


# tester/driver
if __name__ == "__main__":
    model_init()  # builds model of Users
    model_relations()
    # model_print()
