from flask import Blueprint, render_template, request
from projectsearch.projectclass import Projects

projects_object = Projects()

projectsearch_bp = Blueprint('projectsearch', __name__,
                             url_prefix='/projectsearch',
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='assets')


@projectsearch_bp.route('/viewer', methods=["GET", "POST"])
def viewer():
    return render_template('projectsearch.html', projects=projects_object.list)

@projectsearch_bp.route('/details', methods=["GET", "POST"])
def details():
    return render_template('projectdetails.html', project=projects_object.get_details("WASC report"))

@projectsearch_bp.route('/dash', methods=["GET", "POST"])
def dash():
    return render_template('projectdashboard.html', projects=projects_object.list)

@projectsearch_bp.route('/view/<team_selection>/')
def view(team_selection):
    return render_template('projectdetails.html', project=projects_object.get_project(team_selection))
