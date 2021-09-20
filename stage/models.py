from stage import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# class student
class Student(db.Model, UserMixin):
    # Creates the table "Student" in the database
    __tablename__ = "Student"
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(64))
    achternaam = db.Column(db.String(64))
    student_id = db.relationship('RelationTable', backref='Student', uselist=False)
    student_num = db.relationship("User", backref="User", uselist=False)

    def __init__(self, voornaam, achternaam):
        self.voornaam = voornaam
        self.achternaam = achternaam


# class Bedrijf
class Bedrijf(db.Model, UserMixin):
    # Creates the table "Bedrijf" in the database
    __tablename__ = "Bedrijf"
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(64))
    soort = db.Column(db.String(64))
    Bedrijf_id = db.relationship('RelationTable', backref='Bedrijf', uselist=False)

    def __init__(self, naam, soort):
        self.naam = naam
        self.soort = soort
    
    def __repr__(self):
        return f"{self.naam} {self.soort}"


# class Begeleider
class Begeleider(db.Model, UserMixin):
    # Creates the table "Begeleider" in the database
    __tablename__ = "Begeleider"
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(64))
    achternaam = db.Column(db.String(64))
    begeleider_id = db.relationship('RelationTable', backref='Begeleider', uselist=False)

    def __init__(self, voornaam, achternaam):
        self.voornaam = voornaam
        self.achternaam = achternaam
    


# The user_loader decorator provides the user with a flask login and gets the ID of that user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Class User
class User(db.Model, UserMixin):
    # Creates the table "users" in the database
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.String(1))
    student_nr = db.Column(db.Integer, db.ForeignKey("Student.id"))

    def __init__(self, email, username, password, student_nr, admin=0):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.admin = admin
        self.student_nr = student_nr

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Class RelationTable
class RelationTable(db.Model, UserMixin):

    # Creates the table "RelationTable", this table is a collection of all the relationships between tables
    __tablename__ = "RelationTable"
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.Integer,db.ForeignKey('Student.id'))
    bedrijf = db.Column(db.Integer,db.ForeignKey('Bedrijf.id'))
    begeleider = db.Column(db.Integer,db.ForeignKey('Begeleider.id'))
    cijfer = db.Column(db.Integer)
    periode = db.Column(db.String(64))

    def __init__(self, student, bedrijf, begeleider, cijfer, periode):
        self.student = student
        self.bedrijf = bedrijf
        self.begeleider = begeleider
        self.cijfer = cijfer
        self.periode = periode

    def __repr__(self):
        try:
            print(self.Bedrijf.naam)
        except:
            return f"{self.Student.voornaam} {self.Student.achternaam}| - - |{self.Begeleider.voornaam} {self.Begeleider. achternaam} | {self.cijfer}|{self.periode}"
        return f"{self.Student.voornaam} {self.Student.achternaam}|{self.Bedrijf.naam} {self.Bedrijf.soort}|{self.Begeleider.voornaam} {self.Begeleider. achternaam} | {self.cijfer}|{self.periode}"


# Creates all the databases
db.create_all()