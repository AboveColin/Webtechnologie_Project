from flask import Flask, Blueprint,render_template,redirect,url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from stage.models import RelationTable, Student, Bedrijf, db
from stage.administratief.forms import *


administratief_blueprint = Blueprint('administratief',
                              __name__,
                              template_folder='templates/')


# A page for administrators
# Checks if the current user is an administrator
# If yes, the user gets redirected to "index.html"
# If not, the user gets flashed a message
@administratief_blueprint.route("/" )

def administratief():
    return render_template("index.html")


# A page for administrators
# Checks if the current user is an administrator
# If yes, the user gets redirected to "stdnt_home.html"
# If not, the user gets flashed a message 
@administratief_blueprint.route("/student", methods=["GET", "POST"])

def administratief_student():
    return render_template("stdnt_home.html")


# A page for administrators
# Checks if the current user is an administrator
# If yes, the user gets redirected to "beg_home.html"
# If not, the user gets flashed a message 
@administratief_blueprint.route("/begeleider" , methods=["GET", "POST"])

def administratief_begeleider():
    return render_template("beg_home.html")


# A page for administrators
# Checks if the current user is an administrator
# If yes, the user gets redirected to "beg_home.html"
# If not, the user gets flashed a message 
@administratief_blueprint.route("/bedrijven" , methods=["GET", "POST"])

def administratief_bedrijven():
    return render_template("bedr_home.html")


# A page for administrators for adding students
@administratief_blueprint.route("/student/toevoegen", methods=["GET", "POST"])

def administratief_student_add():
    # Checks if the current user is an administrator
    # If yes the user can acces the page
    # If not the user gets flashed a message
    
    # Makes a form where you can select any of the existing "students" "bedrijven" or "begeleider"
    student = Student.query.all()
    bedrijven = Bedrijf.query.all()
    begeleider = Begeleider.query.all()
    form = Student_add() 
    form.student.choices = [x.voornaam for x in student]
    form.bedrijven.choices = [x.naam for x in bedrijven]
    form.begeleider.choices = [x.voornaam for x in begeleider]

    if form.validate_on_submit():
         #Filters on submitted data
        student = Student.query.filter_by(voornaam=form.student.data)
        bedrijf = Bedrijf.query.filter_by(naam=form.bedrijven.data)
        begeleider = Begeleider.query.filter_by(voornaam=form.begeleider.data)
        RelationTable_entry = RelationTable(student=student.first().id, bedrijf=bedrijf.first().id, begeleider=begeleider.first().id, cijfer=form.cijfer.data, periode=form.periode.data)
        db.session.add(RelationTable_entry)
        db.session.commit()
        
        flash("Stage is succesvol gekoppeld aan de student")
        return redirect(url_for("administratief.administratief"))
    return render_template("stdnt_add.html", form=form)


# A page for administrators for editing students
@administratief_blueprint.route("/student/bewerken", methods=["GET", "POST"])

def administratief_student_edit():
    # Checks if the current user is an administrator
    # If yes the user can acces the page
    
    # Makes a form where you can select any of the existing "stage" "bedrijven" or "begeleider"
    stage = RelationTable.query.all()
    bedrijven = Bedrijf.query.all()
    begeleider = Begeleider.query.all()
    form = Student_edit()
    form.student.choices = [x.Student.voornaam for x in stage]
    form.bedrijven.choices = [x.naam for x in bedrijven]
    form.begeleider.choices = [x.voornaam for x in begeleider]
    
    if form.validate_on_submit():
        # Filters on submitted data
        student = form.student.data
        id = RelationTable.query.filter_by(student=Student.query.filter_by(voornaam=student).first().id).first().id
        totaal = RelationTable.query.get(id)
        totaal.bedrijven = Bedrijf.query.filter_by(naam=form.bedrijven.data).first().id
        totaal.begeleider = Begeleider.query.filter_by(voornaam=form.begeleider.data).first().id
        totaal.cijfer = form.cijfer.data
        totaal.periode = form.periode.data
        db.session.commit()
        flash("Stage succesvol bewerkt")
        return redirect(url_for("administratief.administratief"))
    return render_template("stdnt_edit.html", form=form)


# A page for administrators for deleting students
@administratief_blueprint.route("/student/verwijderen", methods=["GET", "POST"])

def administratief_student_del():
    # Checks if the current user is an administrator
    # If yes the user can acces the page
    # If not the user gets flashed a message

    # Makes a form where you can select any of the existing "stage" 
    stage = RelationTable.query.all()
    form = Student_del()
    form.student.choices = [x.Student.voornaam for x in stage]

    if form.validate_on_submit():
        # Filters on submitted data
        student = form.student.data
        naam = RelationTable.query.filter_by(student=Student.query.filter_by(voornaam=student).first().id).first().id
        db.session.delete(RelationTable.query.get(naam))
        db.session.commit()
        flash("Gekoppelde stage succesvol verwijderd van student")
        return redirect(url_for("administratief.administratief"))
    
    totaal_list = []
    for x in stage:
        y = str(x).split('|')
        student= y[0]
        bedrijf = y[1]
        begeleider = y[2]
        cijfer = y[3]
        periode = y[4]
        totaal_list.append([student, bedrijf, begeleider, cijfer, periode])

    return render_template("stdnt_del.html", stages=totaal_list, form=form)


# A page for administrators for deleting students
@administratief_blueprint.route("/student/lijst", methods=["GET", "POST"])

def administratief_student_list():
    # Checks if the current user is an administrator
    # If yes the user can acces the page
    # If not the user gets flashed a message

    # Request all data from table RelationTable
    stage = RelationTable.query.all()
    
    totaal_list = []
    for x in stage:
        y = str(x).split('|')
        student= y[0]
        bedrijf = y[1]
        begeleider = y[2]
        cijfer = y[3]
        periode = y[4]
        totaal_list.append([student, bedrijf, begeleider, cijfer, periode])

    return render_template("stdnt_list.html", stages=totaal_list)


# A page for adding "begeleiders"
@administratief_blueprint.route("/begeleider/toevoegen", methods=["GET", "POST"])

def administratief_begeleider_add():
    
    # Makes a form where you can add a begeleider
    form = Begeleider_add()

    if form.validate_on_submit():
        # Filters on the submitted data
        begeleider = Begeleider(voornaam=form.voornaam.data, achternaam=form.achternaam.data)
        db.session.add(begeleider)
        db.session.commit()
        flash("Begeleider succesvol toegevoegd")
        return redirect(url_for("administratief.administratief"))
    return render_template("beg_add.html", form=form)

# A page for deleting "begeleiders"
@administratief_blueprint.route("/begeleider/verwijderen", methods=["GET", "POST"])

def administratief_begeleider_del():
    
    # Makes a form where you can select a begeleider to delete
    begeleiders = Begeleider.query.all()
    form = Begeleider_del()
    form.begeleider.choices = [x.voornaam for x in begeleiders]

    if form.validate_on_submit():
        # Filters on the submitted data
        voornaam = form.begeleider.data
        begeleider = Begeleider.query.filter_by(voornaam=voornaam).first().id
        db.session.delete(Begeleider.query.get(begeleider))
        db.session.commit()
        flash("Begeleider verwijdering succesvol voltooid!")
        return redirect(url_for("administratief.administratief"))

    return render_template("beg_del.html", begeleiders=begeleiders, form=form)


# A page for adding a company
@administratief_blueprint.route("/bedrijven/toevoegen", methods=["GET", "POST"])

def administratief_bedrijven_add():
    
    # Makes a form where you can add a company
    form = bedrijven_add()
    
    # Submits the given data
    if form.validate_on_submit():
        # Filters on the submitted data
        bedrijf = Bedrijf(naam=form.naam.data, soort=form.soort.data)
        db.session.add(bedrijf)
        db.session.commit()
        flash("Bedrijf succesvol toegevoegd!")
        return redirect(url_for("administratief.administratief"))
    return render_template("bedr_add.html", form=form)


# A pagefor deleting a company
@administratief_blueprint.route("/bedrijven/verwijderen", methods=["GET", "POST"])

def administratief_bedrijven_del():
    
    # Makes a form where you can select a company to delete
    bedrijven = Bedrijf.query.all()
    form = bedrijven_del()
    form.bedrijven.choices = [x.naam for x in bedrijven]
    
    # Submits the given data
    if form.validate_on_submit():
        naam = form.bedrijven.data
        bedrijf = Bedrijf.query.filter_by(naam=naam).first().id
        db.session.delete(Bedrijf.query.get(bedrijf))
        db.session.commit()
        flash("Bedrijf succesvol verwijderd!")
        return redirect(url_for("administratief.administratief"))
    return render_template("bedr_del.html", form=form, bedrijven=bedrijven)