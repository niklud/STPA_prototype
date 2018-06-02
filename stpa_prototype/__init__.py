from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore

from stpa_prototype.auth.auth import auth_blueprint
from stpa_prototype.database.database import db_session, init_db
from stpa_prototype.database.models import User, Role
from stpa_prototype.fundamentals.control_actions import ca_blueprint
from stpa_prototype.fundamentals.goals import goals_blueprint
from stpa_prototype.fundamentals.hazards import hazards_blueprint
from stpa_prototype.fundamentals.pmv import pmv_blueprint
from stpa_prototype.hca.hca import hca_blueprint
from stpa_prototype.project_management.project import project_blueprint
from stpa_prototype.project_management.vcs_blueprint import vcs_blueprint

app = Flask(__name__)

app.config.from_pyfile('../config.py')
# app.db = SQLAlchemy(app)

# Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# # Flask-Login
# login_manager = LoginManager()

app.register_blueprint(goals_blueprint)
app.register_blueprint(hazards_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(vcs_blueprint)
app.register_blueprint(pmv_blueprint)
app.register_blueprint(ca_blueprint)
app.register_blueprint(hca_blueprint)

# init_db()

# # Login manager
# login_manager = LoginManager()
# login_manager.init_app(app)
#
#
# # move later?
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)


# class Todo(app.db.Model):
#     __tablename__ = 'system_goals'
#     id = app.db.Column('todo_id', app.db.Integer, primary_key=True)
#     title = app.db.Column(app.db.String(60))
#     text = app.db.Column(app.db.String)
#     vcs_check = app.db.Column(app.db.Boolean)
#     pub_date = app.db.Column(app.db.DateTime)
#
#     def __init__(self, title, text):
#         self.title = title
#         self.text = text
#         self.vcs_check = False
#         self.pub_date = datetime.utcnow()


# @app.route('/')
# def index():
#     return render_template('index.html', todos=Todo.query.order_by(Todo.id.asc()).all())


@app.route('/')
def hello_world():
    return 'Hello!!!! Werld!'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# if __name__ == '__main__':
#     app.run()
