#**********************
#***Library Includes***
#**********************

from atexit import register
import pytest
import flask_login
# Imports the instance of the web application instantiated in the file "app.py"
from Code import app
from Code.app import app, RegisterForm


#*************************
#***Fixture Definitions***
#*************************


#******************
#***User Story A***
#******************

#*************
#***Test 01***
#************* 

def test_load_login_page():
    '''
    Ensures that the login page successfully loads and is responsive. 
    '''

    # Creates a context object to set up the application context
    context = app.app_context()
    # Appends the context object
    context.push()

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'

    # Initializes a response object to automate testing
    response = app.test_client().get(url, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Tests whether the substring appears in the webpage's output
    # Strings or character arrays need to be passed as "byte strings" when used for comparisons or searches
    assert b'With hands clasped, we cohabitate in close association.' in response.data
    assert b'Hand-in-Hand' in response.data
    assert b'Create new account' in response.data
    assert b'Forgot password?' in response.data
    assert b'Log In' in response.data
    assert b'Mississippi State University | CSE 4214: Introduction to Software Engineering | Group 11' in response.data

    # Deletes the context object
    context.pop()

#*************
#***Test 02***
#*************
def test_valid_user_login_and_logout():
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
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt   

    # <TESTING PLACEHOLDER> : testing statements begi

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                    username = 'js1',
                                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                    first_name = 'James',
                                    middle_name = '',
                                    last_name = 'Smith',
                                    email = 'js1@gmail.com'
                                ))
    

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # In the case of this test, it permits the website to navigate to the user's account from the login page
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/logout'

    # Logs the user out of their account
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Tests whether the substring appears in the webpage's output
    assert b'With hands clasped, we cohabitate in close association.' in response.data
    assert b'Hand-in-Hand' in response.data
    assert b'Create new account' in response.data
    assert b'Forgot password?' in response.data
    assert b'Log In' in response.data
    assert b'Mississippi State University | CSE 4214: Introduction to Software Engineering | Group 11' in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    

    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 03***
#*************
# Does not work; there is an issue with the data being passed to the register form; the test client populates the variables but the web application remains unresponsive
def account_creation():
    '''
    Ensures that the create account feature runs successfully
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import db, User, bcrypt, Flask

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()

    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/register'
    data = {
        "first_name": "John",
        "middle_name": "ddd",
        "last_name": "Doe",
        "username": "jd123",
        "email": "jd123@gmail.com",
        "password": "aA1@sldkepwnwkf",
        "password_confirmation": "aA1@sldkepwnwkf",
    }
    data = dict(
        first_name="John",
        middle_name="ddd",
        last_name="Doe",
        username="jd123",
        email="jd123@gmail.com",
        password="aA1@sldkepwnwkf",
        password_confirmation="aA1@sldkepwnwkf",
    )

    # Does not work
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Tests whether the substring appears in the webpage's output
    assert b'Welcome to Hand-in-Hand! Login to access your account.' in response.data
    assert b'With hands clasped, we cohabitate in close association.' in response.data
    assert b'Hand-in-Hand' in response.data
    assert b'Create new account' in response.data
    assert b'Forgot password?' in response.data
    assert b'Log In' in response.data
    assert b'Mississippi State University | CSE 4214: Introduction to Software Engineering | Group 11' in response.data

    # Cleans the database dropping its tables
    


    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 03***
#*************
def test_valid_credential_retrival():
    '''
    Ensures that a user can generate a new password if they forget their credentials
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1) 

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                    username = 'js1',
                                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                    first_name = 'James',
                                    middle_name = '',
                                    last_name = 'Smith',
                                    email = 'js1@gmail.com'
                                ))
    

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # In the case of this test, it permits the website to navigate to the user's account from the login page
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/logout'

    # Logs the user out of their account
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Tests whether the substring appears in the webpage's output
    assert b'With hands clasped, we cohabitate in close association.' in response.data
    assert b'Hand-in-Hand' in response.data
    assert b'Create new account' in response.data
    assert b'Forgot password?' in response.data
    assert b'Log In' in response.data
    assert b'Mississippi State University | CSE 4214: Introduction to Software Engineering | Group 11' in response.data

    url = '/account_retrieval'

    data=dict(email='js1@gmail.com')

    # Inputs the user's email or username into the forgot credentials prompt
    # Resets the user's password and emails the generated password to their email address 
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'A temporary password has been sent to your email.' in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    
    

    # Deletes the context object
    test_request_context.pop()


#******************
#***User Story b***
#******************

#*************
#***Test 04***
#*************
def test_valid_user_post_and_timeline_visibility():
    '''
    Ensures that a user can access their timeline and post statuses to it
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt   

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                    username = 'js1',
                                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                    first_name = 'James',
                                    middle_name = '',
                                    last_name = 'Smith',
                                    email = 'js1@gmail.com'
                            ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # In the case of this test, it permits the website to navigate to the user's account from the login page
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Imports the database user table "Posts," the random subroutine "randrange," and the datetime function call from the file "app.py"
    from Code.app import Post, randrange, datetime

    # Creates a post used to test the functionality of the user's timeline

    # Generates a unique post id
    new_post_id = randrange(pow(2, 31) - 1)

    # Composes a status using the Post table constructor
    new_post = Post(
        post_id = new_post_id,
        username = "js1",
        post_text = "Test Post #1",
        original_post_time = datetime.now(),
        last_edit_time = None,
        post_media = ""
    )

    # Saves the newly created post into the database
    if (1):
        db.session.add(new_post)
        

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline'

    # Loads the user's timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #1" in response.data
    assert b"js1" in response.data
    assert b"Username" in response.data
    assert b"Original Post Time" in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    
    

    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 05***
#*************
def test_valid_status_deletion_and_editing():
    '''
    Ensures that a user can edit and delete existing statuses
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                    username = 'js1',
                                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                    first_name = 'James',
                                    middle_name = '',
                                    last_name = 'Smith',
                                    email = 'js1@gmail.com'
                                ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Imports the database user table "Posts," the random subroutine "randrange," and the datetime function call from the file "app.py"
    from Code.app import Post, randrange, datetime

    # Creates a post used to test the functionality of the user's timeline

    # Generates a unique post id
    new_post_id = randrange(pow(2, 31) - 1)

    # Composes a status using the Post table constructor
    new_post = Post(
        post_id = new_post_id,
        username = "js1",
        post_text = "Test Post #1",
        original_post_time = datetime.now(),
        last_edit_time = None,
        post_media = ""
    )

    # Saves the newly created post into the database
    if (1):
        db.session.add(new_post)
        

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline'

    # Loads the user's timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #1" in response.data
    assert b"js1" in response.data
    assert b"Username" in response.data
    assert b"Original Post Time" in response.data
    assert b"Edit Time" not in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline/edit_post/' + str(new_post_id)

    data = {
        "edit_text": "Test Post #2",
    }
    
    # Edits an existing post in the user's timeline
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #2" in response.data
    assert b"Test Post #1" not in response.data
    assert b"js1" in response.data
    assert b"Username" in response.data
    assert b"Original Post Time" in response.data
    assert b"Edit Time" in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline/delete_post/' + str(new_post_id)

    # Deletes a user's post
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #2" not in response.data
    assert b"Test Post #1" not in response.data
    assert b"js1" in response.data
    assert b"Username" not in response.data
    assert b"Original Post Time" not in response.data
    assert b"Edit Time" not in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    

    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 06***
#*************
# Source: https://blog.entirely.digital/flask-pytest-testing-uploads/
def test_valid_media_attachment():
    '''
    Ensures that a user can attach media and post to their account
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt 

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                    username = 'js1',
                                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                    first_name = 'James',
                                    middle_name = '',
                                    last_name = 'Smith',
                                    email = 'js1@gmail.com'
                                ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Creates a post used to test the functionality of the user's timeline

    # Imports the library io
    import io

    # Specifics the name of the uploaded file
    # The web application should accpet the file despite it being a textfile
    # The extension is valid, ergo it is accpeted
    filename = "test_file_upload.png"
    # Specifies a byte stream of data
    file_byte_encoding = "iVBORw0KGgoAAAANSUhEUgAAAGoAAABpCAMAAADla0YLAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAi5QTFRFAICAAICAAICAAAAAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICAAICArmZiggAAALp0Uk5TAQQCAAMFGjhigZScnZ6Sf2M7DkCIzvv/+s2HQQlFpflECimw+LEr4eIGe/J9B2n291Xs2ZNlRzo3OUtmVjPb0yHcu3y6UvBaXN/uRt5d/lnFDzwRyQs/dWptdC6kyObH1xQS1hPdENjL5BgZ5cqt8yj0X15MuRYsMdCMCI3Pa1dsDHjrVFMtSsF+NSQiJSYjHVHD8WiA/GBCb5ENZNLj0bdwthdNd6eytbRu6ql26WdI5/UygomKhYb9KbxlqAAABtJJREFUeJztWotXFUUcnr27C4bgC/PiEymproik+AARlUorxZuE+MAyuYJmoUhpLyorXyVXzTIytYeaBZXR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"


    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline/submit_post'
    data = {
        'post_text': "Test Post #1",
        'media': (file_byte_encoding, filename),
    }

    # Posts a status to a user's timeline
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline'

    # Loads the user's timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #1" in response.data
    assert b"js1" in response.data
    assert b"Username" in response.data
    assert b"Original Post Time" in response.data
    assert b"Edit Time" not in response.data
    assert b"test_file_upload.png" in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    db.drop_all()
    

    # Deletes the context object
    test_request_context.pop()


#******************
#***User Story C***
#******************

#*************
#***Test 07***
#*************
def test_sending_friend_request_and_verify_obfuscated_foreign_user_content():
    '''
    Ensures that a user can send a friend request to another user.
    Ensures that the recipient's account is obfuscated, barring the user from viewing their content such as their timeline and friends
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt
        
    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                username = 'jm2',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'Jane',
                                middle_name = '',
                                last_name = 'Meredith',
                                email = 'jm2@gmail.com'
                            ))
    flask_login.login_user(     User   (
                                username = 'js1',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'James',
                                middle_name = '',
                                last_name = 'Smith',
                                email = 'js1@gmail.com'
                            ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "jm2",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b"You can only view jm2\'s account if you are friends" in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("jm2")
    data = {
        'new_relationship_type': "SENT_REQUEST",
    }

    # Sends a friend request from js1 to jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Views the friend page of the current user    
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    

    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 08***
#*************
def test_sent_friend_request_account_changes_accpeting_friend_request_and_removing_friend():
    '''
    Ensures that when the user sends a friend request, that the recipients page acknowledges the request and edits the add friend button to display a different message, namely that the friend request is pending.
    Ensures that when the recipient accepts the friend request that the his or her name is included in the sender's friend list and vice versa.
    Ensures that both users can remove the newly added friend.
    Ensures that once a friend has been removed, the view of the account locks.
    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                username = 'jm2',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'Jane',
                                middle_name = '',
                                last_name = 'Meredith',
                                email = 'jm2@gmail.com'
                            ))
    flask_login.login_user(     User   (
                                username = 'js1',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'James',
                                middle_name = '',
                                last_name = 'Smith',
                                email = 'js1@gmail.com'
                            ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "jm2",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b"You can only view jm2\'s account if you are friends" in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("jm2")
    data = {
        'new_relationship_type': "SENT_REQUEST",
    }

    # Sends a friend request from js1 to jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Sends a friend request from js1 to jm2
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "jm2",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b"Friend request pending" in response.data

    flask_login.login_user(     User   (
                            username = 'jm2',
                            password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                            first_name = 'Jane',
                            middle_name = '',
                            last_name = 'Meredith',
                            email = 'jm2@gmail.com'
                        ))

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "jm2",
        "password": "aA1@sldkepwnwkf",
    }

    # Logs into the user who received the friend request
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'jm2' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Views the friend page of the current user
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data
    assert b'Received friend requests' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("js1")
    data = {
        'new_relationship_type': "SENT_REQUEST",
    }

    # Accepts a friend request
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Views the friend page of the current user
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data
    assert b'Friends' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("js1")
    data = {
        'new_relationship_type': "NO_RELATIONSHIP",
    }

    # Removes a friend
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Views the friend page of the current user
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b'Friends' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "js1",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' not in response.data
    assert b"You can only view js1\'s account if you are friends" in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    
    

    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 09***
#*************
def test_reject_friend_request():
    '''
    Ensures that when the recipient of a friend request declines the offer, that the accounts of both parties acknowledges the decision, removing the notification that a friend request has been sent and the accept/decline offer presented to the recipient.

    '''

    # Imports the instance of the database (db) initialized in the file "app.py"
    from Code.app import db

    # Creates a context object to set up the web application's context
    test_request_context = app.test_request_context()
    # Appends the context object
    test_request_context.push()

    # Builds the database and creates the tables
    db.create_all()

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt   

    # <TESTING PLACEHOLDER> : testing statements begin

    # Directly loggs in a user using the specified paramters
    # The user should only be logged in for the test
    # Source: https://github.com/pytest-dev/pytest-flask/issues/40
    flask_login.login_user(     User   (
                                username = 'jm2',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'Jane',
                                middle_name = '',
                                last_name = 'Meredith',
                                email = 'jm2@gmail.com'
                            ))
    flask_login.login_user(     User   (
                                username = 'js1',
                                password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                                first_name = 'James',
                                middle_name = '',
                                last_name = 'Smith',
                                email = 'js1@gmail.com'
                            ))
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "js123",
        "password": "aA1@sldkepwnwkf",
    }

    # The response statement requires the necessary argument "follow_redirects=True"
    # This allows the web application to load the response page when provided input data
    # Logs the user into their account
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "jm2",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b"You can only view jm2\'s account if you are friends" in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("jm2")
    data = {
        'new_relationship_type': "SENT_REQUEST",
    }

    # Sends a friend request from js1 to jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Sends a friend request from js1 to jm2
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data
    
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "jm2",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' not in response.data
    assert b'jm2' in response.data
    assert b"Friend request pending" in response.data

    flask_login.login_user(     User   (
                            username = 'jm2',
                            password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                            first_name = 'Jane',
                            middle_name = '',
                            last_name = 'Meredith',
                            email = 'jm2@gmail.com'
                        ))

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/login'
    data = {
        "account_identifier": "jm2",
        "password": "aA1@sldkepwnwkf",
    }

    # Logs into the user who received the friend request
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # First, tests whether the web application successfully loaded the page
    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'jm2' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/account/friends'

    # Views the friend page of the current user
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' in response.data
    assert b'Received friend requests' in response.data

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_relationship/' + str("js1")
    data = {
        'new_relationship_type': "NO_RELATIONSHIP",
    }

    # Rejects a friend request
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200

        # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/search'
    data = {
        'search_bar_input': "js1",
    }

    # Searches for the user jm2
    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b'About' in response.data
    assert b'Friends' in response.data
    assert b'Timeline' in response.data
    assert b'Settings' in response.data
    assert b'js1' in response.data
    assert b'jm2' not in response.data
    assert b"You can only view js1\'s account if you are friends" in response.data
    assert b'Send friend request' in response.data
    assert b'Friend request pending' not in response.data

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    
    

    # Deletes the context object
    test_request_context.pop()
