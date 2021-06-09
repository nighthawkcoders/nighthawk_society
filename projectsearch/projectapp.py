from flask import Blueprint, render_template, request
from projectsearch.projectclass import Projects

projects_object = Projects()

projectsearch_bp = Blueprint('projectsearch', __name__,
                       url_prefix='/projectsearch',
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')

projectdetails_bp = Blueprint('projectsearch', __name__,
                       url_prefix='/projectsearch',
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='assets')


@projectsearch_bp.route('/viewer', methods=["GET", "POST"])
def viewer():
    return render_template('projectsearch.html', projects=projects_object.list)

@projectdetails_bp.route('/viewer', methods=["GET", "POST"])
def viewer():
    return render_template('projectsearch.html', projects=projects_object.list)