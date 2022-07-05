# Simple tool used to bootstrap the template with
#   env files since those will be in the .gitignore
#
# This file doesn not need to be modified and it
#   intended to help with project setup

import os.path

DOT_FLASKENV = ".flaskenv"
DOT_ENV = ".env"

def create_dotenv_file():
    if os.path.isfile(DOT_ENV):
        return

    with open(DOT_ENV, 'w') as dotenv:
        dotenv.write("DATABASE=\n")
        dotenv.write("TEST_DATABASE=\n")
        dotenv.write("DBHOST=localhost\n")
        dotenv.write("DBUSERNAME=\n")
        dotenv.write("DBPASSWORD=\n")


def create_dotflaskenv_file():
    if os.path.isfile(DOT_FLASKENV):
        return

    with open(DOT_FLASKENV, 'w') as dotflaskenv:
        dotflaskenv.write(f"FLASK_APP={os.path.join('app', 'main_app.py')}\n")
        dotflaskenv.write("FLASK_ENV=development\n")
        dotflaskenv.write("FLASK_DEBUG=1\n")
        dotflaskenv.write("FLASK_RUN_HOST=localhost\n")
        dotflaskenv.write("FLASK_RUN_PORT=8000\n")


def main():
    print("Bootstrapping Project")
    print(f"Create {DOT_ENV} file")
    create_dotenv_file()
    print(f"Create {DOT_FLASKENV} file")
    create_dotflaskenv_file()


if __name__ == "__main__":
    main()
