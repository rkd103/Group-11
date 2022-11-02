#**********************
#***Library Includes***
#**********************

from atexit import register
import pytest
import flask_login
# Imports the instance of the web application instantiated in the file "app.py"
from Code import app
from Code.app import app, RegisterForm

def test_clean():
    '''
    Ensures that a user can login and logout to his or her account
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables

    # Cleans the database dropping its tables
    db.drop_all()

    # Deletes the context object
    test_request_context.pop()
