from re import X
import mysql.connector


class User:
    def __init__(self, name, id, email, password):
        self._name = name
        self._id = id
        self._email = email
        self._password = password

    def __repr__(self):
        details = f"{self._name}, id {self._id}, email {self._email}"
        if self._id:
            details = f"[id: {self._id}] " + details
        return details

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

class assignment:
    def __init__(self, name):
        self._name = name

    
    def __repr__(self):
        details = f"{self._name}, id {self._id} "
        if self._id:
            details = f"[id: {self._id}] " + details
        return details
    
    @property
    def name(self):
        return self._name


class grades:

    def __init__(self, Assignment_ID, Student_ID, Grade):
        self._Assignment_ID = Assignment_ID
        self._Student_ID = Student_ID
        self._Grade = Grade

    def __repr__(self):
        details = f"Assignment_ID {self._Assignment_ID}, student's ID {self._Student_ID}, grade {self._Grade}"
        if self._Assigment_ID:
            details = f"[student_id: {self._Student_ID}] " + details
        return details

    @property
    def Assignment_ID(self):
        return self._Assignment_ID

    @property
    def Student_ID(self):
        return self._Student_ID

    @property
    def Grade(self):
        return self._Grade


class feedback:
    def __init__(self, assignment_id, student_id, prof_fb, student_resp):
        self._assignment_id = assignment_id
        self._student_id = student_id
        self._prof_fb = prof_fb
        self._student_resp = student_resp
    
    def __repr__(self):
        details = f"Student's ID : {self._student_id}, Assignment's ID {self._assignment_id}, Professor's feedback {self._prof_fb}, Student's response {self._student_resp}"
        return details
    
    @property
    def assignment_id(self):
        return self._assignment_id
    
    @property
    def student_id(self):
        return self._student_id
    
    @property
    def prof_fb(self):
        return self._prof_fb
    
    @property
    def student_resp(self):
        return self._student_resp
    


class class_DB:
    """
    This class provides an interface for interacting with a database of class.
    """
  
    """
    Below are functions to interact with credentials table
    """
    def __init__(self, db_conn, db_cursor):
        self._db_conn = db_conn
        self._db_cursor = db_cursor

    def get_user_info(self, email):
        """
        get user record by email

        :param email: email of the user to look for
        """
        query_name = 'SELECT * FROM credentials WHERE email=%s;'
        cur = self._db_cursor
        cur.execute(query_name, (email, ))
        class_record = cur.fetchone()
        cur.close()
        return class_record

    def add_user(self, new_user):
        """
        Add a new user record to the database

        :param user: new user to be added to the database
        """
        
        insert_user_query = '''
                INSERT INTO credentials (name,id,email,password)
                VALUES (%s, %s, %s,%s);
            '''
    
        cur = self._db_cursor
        cur.execute(insert_user_query, (
                new_user.name,
                new_user.id,
                new_user.email,
                new_user.password,
            ))
        self._db_conn.commit()

            #print(cur.rowcount, "record(s) affected")
    
        #cur.execute("SELECT LAST_INSERT_ID() id")
        new_user_id = cur.fetchone()
    
        cur.close()
        return new_user_id

    def delete_user(self, id):
        """
        Remove a member record from the database

        :param id: id of the member to be removed from the database
        """
        query = 'DELETE FROM credentials WHERE id=%s;'

        cur = self._db_cursor
        cur.execute(query, (id, ))
        self._conn.commit()

        ##print(cur.rowcount, "record(s) affected")
        cur.close()

    def update_user(self, new_user):
        """
        Update a user's record in the database using the name

        :param user: new user to be added to the database
        """

      
        user = self.get_info(new_user.name)
        if user:
            return user
        else:
            query = '''
                UPDATE credentails SET name=%s, id=%s, email=%s, password=%s
                WHERE id=%s;
            '''
    
            cur = self._db_cursor
            cur.execute(
                query,
                (new_user.name, new_user.id, new_user.email, new_user.password))
            self._conn.commit()
    
            print(cur.rowcount, "record(s) affected")
            cur.close()
    
            return self.get_users_by_id(new_user.id)

    def get_user_by_id(self, id):
        """
        Find a user's record in the database using their ID

        :param name: ID of the user
        :return: their name, ID, assignments, and grades
        """

        query = '''
            SELECT * FROM credentials WHERE id=%s;
        '''

        cur = self._db_cursor
        cur.execute(query, (id, ))
        class_record = cur.fetchone()
        #cur.close()
        return class_record
    
    def get_students(self):
        """
        Find all student's whom ID starts with 'S'
        """
        query = '''
            SELECT * FROM credentials WHERE ID LIKE '%S%'; 
        '''
        cur = self._db_cursor
        cur.execute(query)
        record = cur.fetchall()
        return record
        

    def add_assignment(self, new_assignment):
        """
        Add a new assignment record to the database

        :param assignment: new assignment to be added to the database
        """
       
        insert_user_query = '''
                INSERT INTO assignment (assignment_name)
                VALUES (%s);
            '''
        query = '''
                INSERT INTO grades (assignment_ID, student_ID)
                VALUES (%s, %s);
        '''
        query2= '''
                INSERT INTO feedback (assignment_ID, student_ID)
                VALUES (%s, %s);
        '''
        cur = self._db_cursor
        cur.execute(insert_user_query, (
                new_assignment.name,
            ))
        self._db_conn.commit()

            #print(cur.rowcount, "record(s) affected")
    
        cur.execute("SELECT LAST_INSERT_ID() id;")
        new_assignment_id = cur.fetchone()

        for student in self.get_students():
            cur.execute(query, (new_assignment_id['id'], student["ID"]))
            cur.execute(query2, (new_assignment_id['id'], student["ID"]))
            self._db_conn.commit()
        cur.close()
        return new_assignment_id

    def get_assignment_info(self, id):
        """
        Find an assignment's record in the database using its ID

        :param name: ID of the assignment
        :return: the assignment info
        """
        query_name = 'SELECT * FROM assignment WHERE assignment_id=%s;'
        cur = self._db_cursor
        cur.execute(query_name, (id, ))
        class_record = cur.fetchone()
        return class_record
    
    def delete_assignment(self, name):
        """
        Remove an assignment record from the database

        :param name: name of the assignment to be removed from the database
        """
        query = 'DELETE FROM assignment WHERE name=%s;'

        cur = self._conn.cursor()
        cur.execute(query, (name, ))
        self._conn.commit()

        cur.close()
    
    def update_assignment(self, new_assignment):
        """
        Update an assignment's record in the database using the name

        :param user: new assignment to be added to the database
        """

        user = self.get_info(new_assignment.name)
        if user:
            return user
        else:
            query = '''
                UPDATE credentails SET name=%s
                WHERE name=%s;
            '''
    
            cur = self._db_cursor
            cur.execute(
                query,
                (new_assignment.name))
            self._conn.commit()
    
            
            cur.close()
    
            return self.get_assignment_info(new_assignment.name)


    def get_student_grades(self, id):
        """
        Find a student's grade record in the database using the ID of the student

        :param name: ID of the student
        :return: the grade info
        """
        query_name = 'SELECT * FROM grades WHERE Student_ID=%s;'
        cur = self._db_cursor
        cur.execute(query_name, (id, ))
        class_record = cur.fetchone()
        cur.close()
        return class_record


    def add_grade(self, student_id, assignment_id, new_grade):
        """
        Add a new grade to the database
        :param: student's id, assignment's id, and the new grade
        """

        insert_user_query = '''
        UPDATE grades SET Grade=%s WHERE assignment_ID=%s and student_ID=%s;
        '''

        cur = self._db_cursor
        cur.execute(insert_user_query, (
            new_grade,
            assignment_id,
            student_id,
        ))
        self._db_conn.commit()
        cur.execute("SELECT LAST_INSERT_ID() response")
        response = cur.fetchone()
        return response


    def delete_grade(self, Assignment_ID, Student_ID):

        """
        Remove a grade record from the database
        """

        query = 'DELETE FROM grades WHERE Assignment_ID=%s AND Student_ID = %s;'
        cur = self._db_cursor()
        cur.execute(query, (Assignment_ID, Student_ID, ))
        self._conn.commit()
        cur.close()



    def update_grade(self, student_id, assignment_id, new_grade):
        """
        Update a grade's record in the database using the name
        """
        query = '''
        UPDATE grades SET grade=%s
        WHERE Assignment_ID = %s AND Student_ID = %s;
        '''
        cur = self._db_cursor
        cur.execute(query,(
            new_grade,
            assignment_id,
            student_id,
            ))
        #self._conn.commit()
        #cur.close()

        return self.get_users_by_id(student_id)


    def get_grades_by_id(self, student_id):
        """
        Find a grade's record in the database using the student' sID

        :param name: ID of the user
        :return: the grade's info
        """
        query = '''
            SELECT assignment_ID, grade FROM grades WHERE student_ID=%s;
        '''
        cur = self._db_cursor
        cur.execute(query, (student_id, ))
        record = cur.fetchall()
        
        return record
    
    def get_grades_by_aid(self, student_id, assignment_id):
        """
        find a grade's record in the database for a specific sutdent for a specific assignment using the ids
        :param: student's id and the assignment's id
        """
        query = '''
            SELECT * FROM grades WHERE student_ID=%s AND assignment_ID=%s;
        '''
        cur = self._db_cursor
        cur.execute(query, (student_id, assignment_id, ))
        record = cur.fetchall()
        
        return record

    def get_fb_info_by_sid(self, student_id):
        """
        find all feedack's record in the database for a specific sutdent using the ids
        :param: student's id 
        """
        query_name = 'SELECT assignment_ID, professor_feedback, student_response FROM feedback WHERE student_id=%s;'
        cur = self._db_cursor
        cur.execute(query_name, (student_id, ))
        class_record = cur.fetchall()
        
        return class_record
    
    def get_fb_info_by_aid(self, student_id, assignment_id):
        """
        find a feedback's record in the database for a specific sutdent for a specific assignment using the ids
        :param: student's id and the assignment's id
        """
        query_name = 'SELECT * FROM feedback WHERE student_id=%s AND assignment_id=%s;'
        cur = self._db_cursor
        cur.execute(query_name, (student_id, assignment_id,))
        class_record = cur.fetchall()
        
        return class_record
    
    def add_professor_feedback(self, prof_fb, assignment_id, student_id):
        """
        Add a new professor feedback record to the database

        :param user: new professor feedback to be added to the database
        """

        insert_query = """
            UPDATE feedback SET professor_feedback=%s WHERE assignment_ID=%s AND student_ID=%s;
        """
        cur = self._db_cursor
        cur.execute(insert_query, (
            prof_fb,
            assignment_id,
            student_id, 
            ))
        self._db_conn.commit()
        cur.execute("SELECT LAST_INSERT_ID() response")
        response = cur.fetchone()
        return response

    #def add_feedback(self, assignment_ID, student_id, personal_id, feedback)
    def add_student_feedback(self, assignment_id, student_id, student_resp):
        """
        Add a new student feedback to the database

        :param user: new student feedback to be added to the database
        """
        #INSERT INTO feedback (assignment_ID, student_ID, personal_id, student_response)
           # VALUES (%s, %s, %s, %s);
        insert_query = """
            UPDATE feedback SET student_response=%s WHERE assignment_ID=%s AND student_ID = %s;
        """
        cur = self._db_cursor
        cur.execute(insert_query, (
            student_resp,
            assignment_id,
            student_id, 
            ))
        self._db_conn.commit()
        cur.execute("SELECT LAST_INSERT_ID() response")
        response = cur.fetchone()
        cur.close()
        return response
                
    

    def delete_feedback_id(self, assignment_id,student_id):
        """
        delete a feedback record to the database

        :param user: assignment's id and student's id for the feedback to be deleted
        """
        delete_query = """
            DELETE professor_feedback from feedback
            WHERE assignment_id=%s AND student_id=%s;
        """
        cur = self._db_cursor
        cur.execute(delete_query, (assignment_id, student_id, ))
        self._db_conn.commit()
        cur.close()