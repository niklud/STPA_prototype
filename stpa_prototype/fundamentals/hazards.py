from flask import Blueprint, render_template, request, url_for, redirect, session
from stpa_prototype.database.database_project import ProjectDB
from stpa_prototype.database.project_models import Hazard, HCA
from flask_security.decorators import login_required
from stpa_prototype.wtforms.forms import HazardForm

hazards_blueprint = Blueprint('hazards', __name__, template_folder='templates', url_prefix='/hazards')


@hazards_blueprint.route('/')
@login_required
def index():
    project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
    hazards_list = project_db_session.query(Hazard).order_by(Hazard.id.asc()).all()
    project_db_session.close()
    return render_template('fundamentals/hazards/index.html',
                           hazards=hazards_list
                           )


@hazards_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = HazardForm(request.form)
    if request.method == 'POST' and form.validate():
        project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
        hazards = Hazard(form.title.data, form.text.data)
        project_db_session.add(hazards)
        project_db_session.commit()
        project_db_session.close()
        return redirect(url_for('hazards.index'))
    return render_template('fundamentals/hazards/new.html', form=form)


@hazards_blueprint.route('/<hazard_id>', methods=['GET', 'POST'])
@login_required
def show_or_update(hazard_id):
    project_db_session = ProjectDB(session['active_project_db']).get_project_db_session()
    hazard_item = project_db_session.query(Hazard).get(hazard_id)
    hca_list = []
    show_hca = False
    if request.method == 'POST':
        form = HazardForm(request.form)
        if form.show_hca_button.data:
            show_hca = True
            full_hca_list = project_db_session.query(HCA).order_by(HCA.id.asc()).all()
            # hca_list = full_hca_list
            for hca in full_hca_list:
                if hazard_item in hca.cah:
                    hca_list.append(hca)
                elif hazard_item in hca.cah_te:
                    hca_list.append(hca)
                elif hazard_item in hca.cah_tl:
                    hca_list.append(hca)
                elif hazard_item in hca.cah_np:
                    hca_list.append(hca)
        elif form.validate():
            form.populate_obj(hazard_item)
            project_db_session.commit()
            project_db_session.close()
            return redirect(url_for('hazards.index'))
    form = HazardForm(obj=hazard_item)
    # project_db_session.close()
    return render_template('fundamentals/hazards/view.html', form=form, hca_list=hca_list, show_hca=show_hca,
                           hazard_id=hazard_id)
