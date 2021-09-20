from stage import app, db
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from stage.models import *
from stage.forms import *


# This is the home page of the website
@app.route("/")
def home():
    return render_template("home.html")


# Logs out the user and flashes a message
# After logging out it redirects the user to the home page
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("U bent succesvol uitgelogd")
    return redirect(url_for("home"))


# Shows the user a login form
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = Loginform()
    if form.validate_on_submit():
         # Checks if the username is registered in the database
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            # If the username or password isn't recognised, the user gets flashed a message and will be redirected to the login page.
            flash("Inloggen mislukt: gebruikersnaam/wachtwoord niet bekend.")
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html", form=form)


# Shows the registration form
@app.route("/register", methods=["GET", "POST"])
def register():

    # The registration form
    form = Registratie()
    if form.validate_on_submit():

        # Checks if the E-mail or Username is already in use
        # If yes, the user gets flashed a message and will be send back to the registration page
        user_email = User.query.filter_by(email=form.email.data).first()
        user_username = User.query.filter_by(username=form.username.data).first()
        if user_email or user_username:
            flash("E-mailadres of Gebruikersnaam al in gebruik, probeer in te loggen.")
            return redirect(url_for("register"))

        # Creates the variable "student"
        student = Student(voornaam=form.voornaam.data, achternaam=form.achternaam.data)

        # Adds the student to the database
        db.session.add(student)
        db.session.commit()

        # Creates the variable "user"
        user = User(email=form.email.data, username = form.username.data, password = form.password.data, student_nr=student.id)
        # Adds the user to the database
        db.session.add(user)
        db.session.commit()

        flash("Bedankt voor het registreren")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
