import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mijngeheimesleutel'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


from stage.administratief.views import administratief_blueprint
from stage.stage.views import stage_blueprint

# Creeer de blueprints voor de 2 subpagina's.
app.register_blueprint(administratief_blueprint, url_prefix="/administratief")
app.register_blueprint(stage_blueprint, url_prefix="/stage")

login_manager.init_app(app)
login_manager.login_view = "login"

