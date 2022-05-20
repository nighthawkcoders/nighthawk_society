""" database dependencies to support Users db examples """
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along
# Define the many-to-many table associating projects to users

projects_jobs = db.Table('projects_jobs',
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                         db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                         db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'))
                         )

projects_tags = db.Table('projects_tags',
                         db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                         db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                         )


class Note(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
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


# Define the Users table within the model
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

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates an object from U class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_jobs', back_populates='jobs')


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    projects = db.relationship("Project", secondary='projects_tags', back_populates='tags')

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates an object from U class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None


"""Database Creation and Testing section"""


def model_adder(table):
    for row in table:
        try:
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            db.session.remove()
            print("Records exist, duplicate email, or error")


def model_printer(command):
    print("------------")
    print("Table: " + command)
    print("------------")
    result = db.session.execute(command)
    print(result.keys())
    for row in result:
        print(row)


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
        User(name='John Mortensen', email='jmort1021@gmail.com', password='123qwerty', phone="8587754956"),
        User(name='Marie Curie', email='marie@example.com', password='123marie', phone="1111115555"),
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
        Project(name="Area 51",
                scrum_team="Aliens",
                description="Establish project database aliens and relations",
                github_link="http://gihub",
                pages_link="http://pages",
                video_link="http://youtube",
                run_link="http://aws",
                ),
        Project(name="Flintstones",
                scrum_team="Prehistoric Civilization",
                description="Establish project database Flintstones ancestors",
                github_link="http://gihub",
                pages_link="http://pages",
                video_link="http://youtube",
                run_link="http://aws",
                ),
    ]
    model_adder(table)

    area51 = Project.query.filter_by(name="Area 51").first()
    stones = Project.query.filter_by(name="Flintstones").first()

    scrum = Job.query.filter_by(name="Scrum Master").first()
    git = Job.query.filter_by(name="GitHub Admin").first()
    deploy = Job.query.filter_by(name="Deployment Manager").first()
    web = Job.query.filter_by(name="Web Designer").first()
    be = Job.query.filter_by(name="Backend Developer").first()
    area51.jobs.append(scrum)
    area51.jobs.append(git)
    area51.jobs.append(deploy)
    area51.jobs.append(web)
    area51.jobs.append(be)
    stones.jobs.append(scrum)
    stones.jobs.append(git)
    stones.jobs.append(deploy)

    python = Tag.query.filter_by(name="Python").first()
    flask = Tag.query.filter_by(name="Flask").first()
    js = Tag.query.filter_by(name="JavaScript").first()
    area51.tags.append(python)
    area51.tags.append(flask)
    area51.tags.append(js)
    stones.tags.append(js)

    db.session.add(area51)
    db.session.commit()

    print(area51.jobs)
    print(scrum.projects)
    print(be.projects)


def model_print():
    model_printer('select * from users')
    model_printer('select * from jobs')
    model_printer('select * from tags')
    model_printer('select * from projects')
    model_printer('select * from projects_jobs')
    model_printer('select * from projects_tags')


if __name__ == "__main__":
    model_init()  # builds model of Users
    model_print()
