from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import data_required, Email, EqualTo
from wtforms import ValidationError
from stage.models import User, Begeleider

# A form for adding a student and the corresponding information
class Student_add(FlaskForm):
    student = SelectField("Student", validators=[data_required()])
    bedrijven = SelectField("Stage-Bedrijf", validators=[data_required()])
    begeleider = SelectField("Begeleider", validators=[data_required()])
    cijfer = StringField("Cijfer", validators=[data_required()])
    periode = StringField("Periode", validators=[data_required()])
    submit = SubmitField("Voeg toe")


# A form for editing a student and his/her corresponding information
class Student_edit(FlaskForm):
    student = SelectField("Student", validators=[data_required()])
    bedrijven = SelectField("Stage-Bedrijf", validators=[data_required()])
    begeleider = SelectField("Begeleider", validators=[data_required()])
    cijfer = StringField("Cijfer", validators=[data_required()])
    periode = StringField("Periode", validators=[data_required()])
    submit = SubmitField("Bewerk")


# A form for deleting a student
class Student_del(FlaskForm):
    student = SelectField("Student", validators={data_required()})
    submit = SubmitField("Verwijder")


# A form for adding a company and its corresponding information
class bedrijven_add(FlaskForm):
    naam = StringField("Naam bedrijf", validators=[data_required()])
    soort = SelectField("Soort bedrijf", validators=[data_required()], choices=["Servicedesk", "Media", "ICT", "Zorg", "Techniek"])
    submit = SubmitField("Toevoegen")

# A form for deleting a company 
class bedrijven_del(FlaskForm):
    bedrijven = SelectField("Stage", validators=[data_required()])
    submit = SubmitField("Verwijder")


# A form for adding a "begeleider"
class Begeleider_add(FlaskForm):
    voornaam = StringField("Voornaam", validators=[data_required()])
    achternaam = StringField("Achternaam", validators=[data_required()])
    submit = SubmitField("Voeg toe")


# A form for deleting a "begeleider"
class Begeleider_del(FlaskForm):
    begeleider = SelectField("Begeleider", validators=[data_required()])
    submit = SubmitField("Verwijder")
