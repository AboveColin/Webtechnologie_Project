from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import data_required, Email, EqualTo
from wtforms import ValidationError
from stage.models import User, Begeleider

# A form where a user can login using a submit button, his username and password.
class Loginform(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[data_required()])
    password = PasswordField("Wachtwoord", validators=[data_required()])
    submit = SubmitField("Inloggen")


# A form where you can register as a user
class Registratie(FlaskForm):
    email = StringField("E-mailadres", validators=[data_required(), Email()])
    voornaam = StringField("Voornaam", validators=[data_required()])
    achternaam = StringField("Achternaam", validators=[data_required()])
    username = StringField("Gebruikersnaam", validators=[data_required()])
    password = PasswordField("Wachtwoord", validators=[data_required(), EqualTo("pass_confirm", message="Wachtwoorden komen niet overeen")])
    pass_confirm = PasswordField("Bevestig wachtwoord", validators=[data_required()])
    submit = SubmitField("Registreer")


