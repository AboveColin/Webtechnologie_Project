from flask import Flask, Blueprint,render_template,redirect,url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from stage.models import *
from stage.forms import *


stage_blueprint = Blueprint('stage',
                              __name__,
                              template_folder='templates/')


# Sends you to the stageplekken page
@stage_blueprint.route("/")
def stages():

    # Shows the corresponding stageplek of the user
    stage = RelationTable.query.all()
    bedrijf = Bedrijf.query.all()

    if current_user.is_authenticated:

        # Filters on the given data
        id = RelationTable.query.filter_by(student=current_user.student_nr).first()
        if id:
            User_data = []
            user = RelationTable.query.get(id.id)
            x = str(user).split('|')
            student= x[0]
            bedrijf = x[1]
            begeleider = x[2]
            cijfer = x[3]
            periode = x[4]
            User_data.append([student, bedrijf, begeleider, cijfer, periode])
            return render_template("stage.html", bedrijf=bedrijf, stage=stage, totaal=User_data[0])
    return render_template("stage.html", bedrijf=bedrijf, stage=stage)