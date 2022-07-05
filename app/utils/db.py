"""
Collection of functions to help establish the database
"""
import mysql.connector


# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        ''' 
        CREATE TABLE credentials
        (
            name VARCHAR(100),
            ID VARCHAR(100),
            email VARCHAR(50),
            password VARCHAR(50),
            CONSTRAINT pk_student_id PRIMARY KEY (ID)
        );
        '''
    )

    cursor.execute(
        ''' 
        CREATE TABLE assignment
        (
            assignment_name VARCHAR(50),
            assignment_id TINYINT UNSIGNED AUTO_INCREMENT,
            CONSTRAINT pk_assignment PRIMARY KEY (assignment_id)
        );
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE grades
        (
            assignment_ID TINYINT UNSIGNED,
            student_ID VARCHAR(50),
            grade TINYINT UNSIGNED,
            CONSTRAINT fk_student_id FOREIGN KEY (student_ID)
              REFERENCES credentials (ID)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_assignment_id FOREIGN KEY (assignment_ID)
              REFERENCES assignment (assignment_id)
            ON DELETE RESTRICT ON UPDATE CASCADE
        );
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE feedback
        (
            assignment_ID TINYINT UNSIGNED,
            student_ID VARCHAR(50),
            professor_feedback VARCHAR(250),
            student_response VARCHAR(250),
            CONSTRAINT fk_assignment_i FOREIGN KEY (assignment_ID)
              REFERENCES assignment (assignment_id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT fk_student_i FOREIGN KEY (student_ID)
              REFERENCES credentials (ID)
            ON DELETE RESTRICT ON UPDATE CASCADE
        );
        '''
    )
    cursor.close()
    conn.close()
