"""
task_api.py

Routes for the API and logic for managing Tasks.
"""

from flask import g, request, jsonify, Blueprint

from models.task import class_DB, User, assignment, grades, feedback

# Establish the blueprint to link it to the flask app file (main_app.py)
#   Need to do this before you create your routes
task_api_blueprint = Blueprint("task_api_blueprint", __name__)


# Define routes for the API
#   Note that we can stack the decorators to associate similar routes to the same function.
#   In the case below we can optionally add the id number for a task to the end of the url
#   so we can retrieve a specific task or the entire list of tasks as a JSON object
@task_api_blueprint.route('/api/v1/user/', defaults={'ID':None}, methods=["GET","POST","PUT"])
@task_api_blueprint.route('/api/v1/user/<string:ID>/', methods=["GET","POST","PUT"])
def get_user(ID):
    """
    get_tasks can take urls in a variety of forms:
        * /api/v1/task/ - get all tasks
        * /api/v1/task/1 - get the task with id 1 (or any other valid id)
        * /api/v1/task/?search="eggs" - find all tasks with the string "eggs" anywhere in the description
            * The ? means we have a query string which is essentially a list of key, value pairs
                where the ? indicates the start of the query string parameters and the pairs are separated
                by ampersands like so:
                ?id=10&name=Sarah&job=developer
            * The query string is optional 
    """

    # To access a query string, we need to get the arguments from our web request object
    args = request.args
    
    # setup the TaskDB object with the mysql connection and cursor objects
    appdb = class_DB(g.mysql_db, g.mysql_cursor)

    result = None
    
    # If an ID for the task is not supplied then we are either returning all
    #   tasks or any tasks that match the search query string.
    if ID is None:
        # Logic to find all or multiple tasks

        # Since the args for the query string are in the form of a dictionary, we can
        #   simply check if the key is in the dictionary. If not, the web request simply
        #   did not supply this information.
        if not 'search' in args:
            result = appdb.get_user_by_id(ID)
    
    else:
        # Logic to request a specific task
        # We get a specific tasks based on the provided task ID
        result = appdb.get_user_by_id(ID)

    # Sending a response of JSON including a human readable status message,
    #   list of the tasks found, and a HTTP status code (200 OK).
    return jsonify({"users": result}), 200


@task_api_blueprint.route('/api/v1/tasks/', methods=["GET","POST","PUT"])
def add_user():
    appdb = class_DB(g.mysql_db, g.mysql_cursor)
    user = User(request.json['name'],request.json['ID'],request.json['email'],request.json['password'])
    result = appdb.add_user(user)
    
    return jsonify({"name": result['name'], "ID": result['ID'], "email": result['email'], "password": result['password']}), 200

"""
@task_api_blueprint.route('/api/v1/tasks/<int:task_id>/', methods=["PUT"])
def update_task(task_id):
    taskdb = TaskDB(g.mysql_db, g.mysql_cursor)

    task = Task(request.json['description'])
    taskdb.update_task(task_id, task)
    
    return jsonify({"status": "success", "id": task_id}), 200


@task_api_blueprint.route('/api/v1/tasks/<int:task_id>/', methods=["DELETE"])
def delete_task(task_id):
    taskdb = TaskDB(g.mysql_db, g.mysql_cursor)

    taskdb.delete_task_by_id(task_id)
        
    return jsonify({"status": "success", "id": task_id}), 200
    """
