"""
conftest.py

Supplies the necessary testing fixtures to allow for simulated testing of the flask
application (see test_task_api.py) or database (see test_taskdb.py). Any tests for 
classes that do not require either the flask application or the database can be tested
without using the fixtures below as test function parameters (see test_task.py).

********* DO NOT MIX FIXTURES WITHIN THE SAME PYTHON TEST FILE *ßßßßß*********************

"""
import os
import sys

# Need to append the root of the app to the Python path
# to make imports work as intended
sys.path.append('app/')

import pytest
from dotenv import load_dotenv

# We need to import fun_app so that we can access the app instance
import app.main_app as main_app
import app.utils.db as UtilsDB

# Here is a custom pytest fixture which yields a Flask test client which is
# connected to the app and can simulate requests. Any test function in this
# module that has a parameter named flask_test_client will automatically be passed
# the flask test app. The database and the flask app maintain state per test file.
@pytest.fixture(scope='module')
def flask_test_client():
    main_app.app.config["DATABASE"] = os.getenv("TEST_DATABASE")
    # This enables testing mode for the app
    main_app.app.testing = True
    # A test client provides methods for simulating requests to the app
    test_client = main_app.app.test_client()

    # In order to call the init_db() function from task_app.py, we need to set
    # up an application context.
    with main_app.app.app_context():
        UtilsDB.init_db(main_app.app.config)

    # Any function using this fixture will be passed test_client
    #   What's a yield?
    #       For our purposes, the yield will hand off the test_client to all
    #       the test cases in a file. When they are have all been executed and
    #       are done using it, we come back to the yield and continue execution.
    yield test_client


# This fixture is used for database tests to load a test database in MySQL.
# Any test function in this module that has a parameter named db_test_client
# will automatically be passed a MySQL connection. The database maintains state
# per test file.
@pytest.fixture(scope='module')
def db_test_client():
    load_dotenv()

    config = {
        "DBHOST": os.getenv("DBHOST"),
        "DATABASE": os.getenv("TEST_DATABASE"),
        "DBUSERNAME": os.getenv("DBUSERNAME"),
        "DBPASSWORD": os.getenv("DBPASSWORD")
    }

    UtilsDB.init_db(config)
    conn = UtilsDB.connect_db(config)
    cursor = conn.cursor(dictionary=True)

    # Give the connection and cursor to the tests that use this fixture
    yield conn, cursor

    # Clean-up the resources when we are done with all tests in a file
    cursor.close()
    conn.close()