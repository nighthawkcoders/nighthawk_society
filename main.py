from flask import Flask, render_template, request, redirect, url_for
from models.lessons import MenuData
import requests
from y2021 import y2021_bp
from y2021.prep import y2021_prep_bp
from y2021.tri1 import y2021_tri1_bp
from y2021.tri2 import y2021_tri2_bp
from y2021.tri3 import y2021_tri3_bp

app = Flask(__name__)
app.register_blueprint(y2021_bp, url_prefix='/y2021/repos')
app.register_blueprint(y2021_prep_bp, url_prefix='/y2021/prep')
app.register_blueprint(y2021_tri1_bp, url_prefix='/y2021/tri1')
app.register_blueprint(y2021_tri2_bp, url_prefix='/y2021/tri2')
app.register_blueprint(y2021_tri3_bp, url_prefix='/y2021/tri3')
# md is an object that contains data for menus
md = MenuData()


@app.route('/')
def index():
    print(MenuData.menus)
    return render_template("homesite/index.html", menus=md.menus)


"""Landing page from Menu selection"""


@app.route('/landing/<selection>/', methods=['GET', 'POST'])
def landing(selection):
    # POST redirection to content page
    if request.method == 'POST':
        form = request.form
        selection = form['page']
        try:  # allows for direct route
            return redirect(url_for(selection))
        except:  # else the routes are handled by lesson select below
            return redirect(url_for("lesson", selection=selection))
    # GET landing page render based off of "selection"
    heading, projects = md.get_menu(selection)
    return render_template("homesite/landing.html", heading=heading, projects=projects)


"""Lesson from enumerated button selection"""


@app.route('/lesson/<selection>/')
def lesson(selection):
    x = requests.get('https://w3schools.com/python/demopage.htm')
    print(x.text)
    return render_template("homesite/lesson.html", data=md.get_lesson(selection))


if __name__ == "__main__":
    # runs the application on the repl development server
    app.run(debug=True)
