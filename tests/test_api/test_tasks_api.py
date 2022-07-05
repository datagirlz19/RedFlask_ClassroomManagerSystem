import json


# By using the parameter flask_test_client, we automatically get access to a "fake" version
#   of our webservice application to test our api. This is provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_posting_a_user(flask_test_client):

    # Simulate a post request that sends json data
    request = flask_test_client.post('api/v1/user/', json={'name': 'student',
                                                            'ID' : 'S-1',
                                                            'email' : 'student@wooster.edu',
                                                            'password' : 'password'
                                                            })

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    #   object. The json object can be treated similarly to a dictionary or list
    #   based on the format of the JSON content.
    data = json.loads(request.data.decode())
    assert data["ID"] == "S-1"

    request = flask_test_client.post('api/v1/user/', json={'name': 'professor',
                                                            'ID' : 'P-1',
                                                            'email' : 'professor@wooster.edu',
                                                            'password' : 'password'
                                                            })

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    assert data['ID'] == "P-1"

"""
def test_get_all_tasks(flask_test_client):
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/tasks/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['tasks']) == 2

    # When getting all the tasks, we cannot rely on the ordering because I did
    #   not enforce an ordering on the SQL query. Always be careful with
    #   assumptions about order unless you have explicity
    #   ensured that the content will be ordered
    for task in data['tasks']:
        if task['id'] == 1:
            assert task['description'] == 'first task'
        elif task['id'] == 2:
            assert task['description'] == 'second task'
        else:
            # We should not get here as there are only two items inserted
            raise Exception("Unknown task found in database!")


def test_get_user_by_id(flask_test_client):
    
    # Here is how to use the test client to simulate a GET request
    request = flask_test_client.get('/api/v1/tasks/S-1/')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    #assert len(data['user']) == 1

    # Get the first item from the list of tasks (which should only be task id 1)
    task = data['user'][0]

    # Check the id and description
    assert task['id'] == "S-1"
    assert task['name'] == 'student'


def test_get_task_by_description_search(flask_test_client):

    # Here is how to use the test client to simulate a GET request with a query string
    request = flask_test_client.get('/api/v1/tasks/?search=second')

    # The body of the response is JSON, so we turn it from a string into a JSON
    # object.
    data = json.loads(request.data.decode())

    # Make sure we got a status code of 200
    assert request.status_code == 200

    # Verify data
    assert len(data['tasks']) == 1

    # Since I know this test should only return one value I can request
    #   the task from the list of tasks via its index
    task = data['tasks'][0]

    assert task['id'] == 2
    assert task['description'] == 'second task'


def test_update_task_by_id(flask_test_client):
    
    # Add a new task to the list
    request = flask_test_client.post('/api/v1/tasks/', json={'description': 'task to be updated'})
    assert request.status_code == 200
    
    data = json.loads(request.data.decode())
    task_id = data['id']

    # Here is how to use the test client to simulate a PUT request
    request = flask_test_client.put(f'/api/v1/tasks/{task_id}/', json={'description': 'updated via test'})
    
    # Make sure we got a status code of 200
    assert request.status_code == 200

    data = json.loads(request.data.decode())
    assert task_id == data['id']

    request = flask_test_client.get(f'/api/v1/tasks/{task_id}/')
    data = json.loads(request.data.decode())

    task = data['tasks'][0]
    assert task['id'] == task_id
    assert task['description'] == 'updated via test'
"""