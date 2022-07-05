from app.models.task import class_DB
"""
# By using the parameter db_test_client, we automatically get access to our test
#   database provided by the pytest fixture in conftest.py
#   (note the parameter name matches the name of the fixture function).
def test_task_insert(db_test_client):
    # The test fixture only setups the 
    conn, cursor = db_test_client
    taskdb = TaskDB(conn, cursor)

    taskdb.insert_task(Task("Hi there"))
    
    result = taskdb.select_task_by_id(1)[0]
    assert result['description'] == "Hi there"
    conn.commit()


def test_task_delete(db_test_client):
    conn, cursor = db_test_client
    taskdb = TaskDB(conn, cursor)
    
    taskdb.insert_task(Task("Delete Me!"))

    result = taskdb.select_task_by_id(2)[0]
    assert result['description'] == "Delete Me!"

    taskdb.delete_task_by_id(2)
    result = taskdb.select_task_by_id(2)
    assert len(result) == 0
    conn.commit()

"""