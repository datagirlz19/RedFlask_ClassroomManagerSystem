# Final Project Name
Red Flask - Moodle but better

## Description
This software application that we develop will assist students communicate with their professors better, as well as the students' performance will be easier to access and view. In our application, students will be able to see their own information (grades, assignments, student's name, student's ID, etc), and add their response to the grades that professors post for each assignment. Professors's view is more broad. They can add, delete, update assignments/grades/students information. They will also can add feedback for each assignment that they grade for each student.

In order to run the application, the customer will have to:
1) Open a new terminal
2) Run command: python3 -m venv env
3) Run command: source env/bin/activate
4) Run command: pip install -r requirements.txt
5) Run command: flask initdb
6) Run command: flask run
=> The terminal will pop up a link in the line "Running on http:///localhost:8000/, click on this link. You are at our website now!

Once you get to our website, if you already have an account, please log in. If not, you can sign up and follow the instruction on the website to fill in your ID (so that you can retrieve the student or professor view correctly). After you log in/sign up, you will be able to complete every action below!

## API Documentation
1) Add new user:
We can add new user (professor or student) along with their information: name, ID, email, password
2) Delete user:
We can delete the user's information completely from the database
3) Get user (both Professors and Students) information:
Retrieve user's information (name, ID, email)
4) Update user:
Users will be able to update their name, ID, email, and password in the database if they want to
5) Add assignment:
Professors will be able to add new assignment into the database, the assignment ID will be automatically incremented
6) Get assignment information:
Users will be able to retrieve information about assignments (assignment name and asisgnment ID)
7) Update assignment:
Professors will be able to change/update the assignments' names
8) Delete assignment:
Professors will be able to delete assignments and every information that related to those assignments in the database
9) Add grade:
Professor will be able to add grade for every assignment for every student
10) Update grade:
Professor will be able to change/update grade(s) for their students
11) Delete grade:
Professor will be able to delete grade(s) that they uploaded
12) Get grades by ID:
Students will be able to only see their grades based on their student ID. Professors can view everyone's grades and their ID.
13) Add Professors Feedback:
Professors will be able to add their feedback for every assignment for every student
14) Update Professors Feedback:
Professors will be able to change/update their feedback for every assignment for every student
15) Delete Professors Feedback:
Professors will be able to delete their feedback for every assignment for every student
16) Add Students Response:
Students will be able to add their response for every assignment that is graded and maybe feedback by their Professors
17) Update Students Response:
Students will be able to change/update their response for every assignment that is graded and maybe feedback by their Professors
18) Delete Students Response:
Students will be able to delete their response for every assignment that is graded and maybe feedback by their Professors



