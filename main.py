from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3 as sl3

from models.lessons import LessonData
from projectsearch.projectapp import projectsearch_bp
from projectsearch.projectapp import projectdetails_bp

app = Flask(__name__)  # app is the main flask object
#import storecom
#import connection
ld = LessonData()  # ld is an object that contains data for lesson


@app.route('/')
def index():
    return render_template("homesite/index.html", menus=ld.menus)


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
    heading, projects = ld.get_menu(selection)
    return render_template("homesite/landing.html", heading=heading, projects=projects)


"""Lesson from enumerated button selection"""


@app.route('/lesson/<selection>/')
def lesson(selection):
    x = requests.get('https://w3schools.com/python/demopage.htm')
    print(x.text)
    return render_template("homesite/lesson.html", data=ld.get_lesson(selection))

#@app.route('/projectsri')
#def projectsri():
    #return render_template("projectsearch.html")

@app.route('/projectdetails')
def projectdetails():
    return render_template("projectdetails.html")

@app.route('/projectsearch/comment/')
def comment():
    first = request.form.get("who", False)
    second= request.form.get("message", False)
    conn = sl3.connect('walrus.db')
    c = conn.cursor()
    c.execute("SELECT * FROM COMMENTS")
    comment.storecom(first,second)
    return render_template("comment.html", com=c.fetchall())


app.register_blueprint(projectsearch_bp)
#app.register_blueprint(projectdetails_bp)


#for comment section
#@app.route('/comments')
#def comments():
#   return 'Comments'
#for submitting comment

#@app.route('submit_comments', methods=['POST'])
#def submit_comments():
#   comment = {
# 'body': request.form['comment'],
#'name':request.form['name']
#   }
#database.post('/comments',comment)
# return redirect(url_for('comments'))


if __name__ == "__main__":
    # runs the flask application on the repl development server
    app.run(debug=True)
