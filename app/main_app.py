"""
main_app.py

All core flask application functionality ties here including:
    * App configuration settings ()
    * Commandline functionality to initialize a database
    * Database access for each request
    * Registration for all routes (via blueprints)


To keep this code brief there is no handling of errors or bad requests
"""

# Imports for all built-in python libraries
import os
import uuid

# Imports all 3rd-party libraries
from flask import Flask, g, session
from dotenv import load_dotenv
from flask_session import Session

# Imports for blueprints and other modules written for the application
from views.task_view import task_list_blueprint
from api.task_api import task_api_blueprint
import utils.db as DBUtils

# Load all the private data from the 
#   .env and .flaskenv files into our
#   environment variables
load_dotenv()

# Create an instance of the flask application
#   this is our webservice
app = Flask(__name__)

# Add some configuration data to your application
#   to easily access important start up data
# In our case here, we are using this app.config
#   dictionary to setup database connection information
app.config["DATABASE"] = os.getenv("DATABASE")
app.config["DBHOST"] = os.getenv("DBHOST")
app.config["DBUSERNAME"] = os.getenv("DBUSERNAME")
app.config["DBPASSWORD"] = os.getenv("DBPASSWORD")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Useful if you decide to create session cookies
#   (the CS50 video discusses sessions)
app.config["SECRET_KEY"] = uuid.uuid4().hex

# Setup Views
app.register_blueprint(task_list_blueprint)
app.register_blueprint(task_api_blueprint)


# Helper function to establish a connection to the database
def connect_db():
    # g is a special variable provided by flask
    #   to provided temporary access to data globally.
    #   In this case, we are using g to provide the MySQL
    #   database connection and cursor objects for each
    #   request made to our site.
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = DBUtils.connect_db(app.config)
    if not hasattr(g, 'mysql_cursor'):
        g.mysql_cursor = g.mysql_db.cursor(dictionary=True)


# Helper function to release the connection to the database
def disconnect_db():
    g.mysql_cursor.close()
    g.mysql_db.close()


# This is a command that you can add to the flask application
# You can run:
#   flask initdb
# which will run the function and in this case setup the database
@app.cli.command('initdb')
def initdb_cli_command():
    DBUtils.init_db(app.config)


# Function called before all requests to the webservice
@app.before_request
def before():
    connect_db()


# Function called after the completion of a webservice request
@app.after_request
def after(response):
    disconnect_db()
    return response
