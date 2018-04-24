from flask import Blueprint, render_template, request, url_for, redirect, session
# from flask import current_app as app
# from stpa_prototype.database.database import db_session
from stpa_prototype.database.database_project import ProjectDB
from stpa_prototype.database.models import Goal
from flask_security.decorators import login_required

goals_blueprint = Blueprint('goals', __name__, template_folder='templates', url_prefix='/goals')


@goals_blueprint.route('/hello')
def hello_world():
    return 'Hello!!!! Werld!'


@goals_blueprint.route('/test')
def test():
    print session['active_project_db']
    db = ProjectDB(session['active_project_db']).get_project_db_session()
    db.add(Goal('thisistest', 'still test'))
    db.query(Goal).all()
    return 'Hello!!!! Werld!'


@goals_blueprint.route('/')
@login_required
def index():
    project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
    return render_template('fundamentals/goals/index.html',
                           goals=project_db_session.query(Goal).order_by(Goal.id.asc()).all()
                           )


@goals_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
        goals = Goal(request.form['title'], request.form['text'])
        project_db_session.add(goals)
        project_db_session.commit()
        return redirect(url_for('goals.index'))
    return render_template('fundamentals/goals/new.html')


@goals_blueprint.route('/<goal_id>', methods=['GET', 'POST'])
@login_required
def show_or_update(goal_id):
    project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
    goal_item = Goal.query.get(goal_id)
    if request.method == 'GET':
        return render_template('fundamentals/goals/view.html', goal=goal_item)
    goal_item.title = request.form['title']
    goal_item.text = request.form['text']
    goal_item.vcs_check = ('vcs_check.%d' % goal_id) in request.form
    project_db_session.commit()
    return redirect(url_for('goals.index'))
