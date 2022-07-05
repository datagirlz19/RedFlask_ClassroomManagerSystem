from crypt import methods
from functools import reduce
from flask import Blueprint, request, redirect, session
from flask import render_template, g, Blueprint
from flask_session import Session
from api.task_api import User, class_DB, assignment

task_list_blueprint = Blueprint('task_list_blueprint', __name__)

@task_list_blueprint.route('/', methods=["GET", "POST"])
def index():
    if not session.get("id"):
        return redirect("/login")
    return render_template("index.html")

@task_list_blueprint.route('/login', methods=["GET"])
def login():
    return render_template("login.html")

@task_list_blueprint.route('/check_credential', methods=["POST"])
def check_cred():
    user_email = request.form.get("email")
    user_password = request.form.get("password")
    database = class_DB(g.mysql_db, g.mysql_cursor)
    user = database.get_user_info(user_email)
    if user and user["password"] == user_password:
        session["id"] = user["ID"]
        session["name"] = user["name"]
        return redirect("/feedback_view")
    else:
        return redirect('/signup')


@task_list_blueprint.route("/logout")
def logout():
    session["name"] = None
    session["id"] = None
    return redirect('/')

@task_list_blueprint.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@task_list_blueprint.route("/add_user", methods=["POST"])
def add_user():
    user_name = request.form.get("name")
    user_id = request.form.get("id")
    user_email = request.form.get("email")
    user_password = request.form.get("password")

    new_user = User(user_name, user_id, user_email, user_password)
    database = class_DB(g.mysql_db, g.mysql_cursor)

    database.add_user(new_user)

    return redirect("/login")

@task_list_blueprint.route("/feedback_view", methods=["GET", "POST"])
def student_view():
    id = session["id"][0]
    if id.lower() == 's':
        database = class_DB(g.mysql_db, g.mysql_cursor)
        assignment_list = database.get_fb_info_by_sid(session["id"])
        grades = database.get_grades_by_id(session["id"])
        return render_template("student_assignment.html", assignment_list=assignment_list, grades=grades)
    if id.lower() == 'p':
        return render_template("prof_view.html")

@task_list_blueprint.route("/studentlist", methods=["GET","POST"])
def student_list():
    database = class_DB(g.mysql_db, g.mysql_cursor)
    students = database.get_students()
    return render_template("student_list.html", students=students)

@task_list_blueprint.route("/addassignment", methods=["GET"])
def add_assignment_view():
    return render_template("add_assignment.html")

@task_list_blueprint.route("/add_assignment", methods=["POST"])
def add_assignment():
    database = class_DB(g.mysql_db, g.mysql_cursor)
    assignment_name = request.form.get("name")
    new_assignment = assignment(assignment_name)
    database.add_assignment(new_assignment)
    return redirect("/feedback_view")
    

@task_list_blueprint.route("/students_asgn_prof", methods=["GET", "POST"])
def students_asgn_prof():
    database = class_DB(g.mysql_db, g.mysql_cursor)
    student_id = request.form.get("student_ID")
    session["stud_selected"] = student_id
    assignment_list = database.get_fb_info_by_sid(student_id)
    grades = database.get_grades_by_id(student_id)
    return render_template("students_asgn_prof.html", assignment_list=assignment_list, grades=grades)

@task_list_blueprint.route("/addresponse", methods=["GET", "POST"])
def addresponse():
    database = class_DB(g.mysql_db, g.mysql_cursor)
    assignment_id = request.form.getlist("assignment_ID")
    response = request.form.get("response")
    for id in assignment_id:
        database.add_student_feedback(id,session["id"],response)
    return redirect('/feedback_view')

@task_list_blueprint.route("/addgr_fb", methods=["GET","POST"])
def addgr_fb():
    database = class_DB(g.mysql_db, g.mysql_cursor)
    assignment_id = request.form.getlist("assignment_ID")
    grade = request.form.get("grade")
    feedback = request.form.get("feedback")
    student_id = session["stud_selected"]
    for id in assignment_id:
        if feedback:
            database.add_professor_feedback(feedback, id, student_id)
        if grade:
            database.add_grade(student_id, id, int(grade))
    return redirect('/feedback_view')