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
        "account_identifier": "js1",
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
    db.drop_all()

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
        "account_identifier": "js1",
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
    db.drop_all()

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
        "account_identifier": "js1",
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
        "account_identifier": "js1",
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
        "account_identifier": "js1",
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
    filename = "test_file_upload.txt"
    # Specifies a byte stream of data
    file_byte_encoding = (io.BytesIO(b"iVBORw0KGgoAAAAo3OUtmVjPb0yHcu3y6UvBaXN/uRt5d/lnFDzwRyQs/dWptdC6kyObH1xQS1hPdENjL5BgZ5cqt8yj0X15MuRYsMdCM"))

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/home/timeline/submit_post'
    data = {
        'post_text': "Test Post #1",
        'media': (file_byte_encoding, filename),
    }

    # Fails to post a status to the user's timeline due to an incorrect file extension
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
    assert b"Test Post #1" not in response.data
    assert b"js1" in response.data
    assert b"Username" not in response.data
    assert b"Original Post Time" not in response.data
    assert b"Edit Time" not in response.data
    assert b"test_file_upload.txt" not in response.data

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
        
    # <TESTING PLACEHOLDER> : testing statements begin

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

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
        "account_identifier": "js1",
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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "js1", username_2 = "jm2",
                                        relationship_type = RelationshipType.FRIEND
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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
    db.drop_all()


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

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)

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
        "account_identifier": "js1",
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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "jm2", username_2 = "js1",
                                        relationship_type = RelationshipType.RECEIVED_REQUEST
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "js1", username_2 = "jm2",
                                        relationship_type = RelationshipType.FRIEND
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()

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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Retrieves the relationship created between the user's "js1" and "jm2"
    current_relationship = Relationship.query.filter_by (
                                                            username_1 = "js1", username_2 = "jm2"
                                                        ).first()
    
    # Deletes the created relationship from the database and saves its state
    db.session.delete(current_relationship)
    db.session.commit()

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
    assert b'<div id="friends">\n        \n\n        \n    </div>' in response.data
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
    db.drop_all()

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

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

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
        "account_identifier": "js1",
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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "jm2", username_2 = "js1",
                                        relationship_type = RelationshipType.RECEIVED_REQUEST
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Retrieves the relationship created between the user's "js1" and "jm2"
    current_relationship = Relationship.query.filter_by (
                                                            username_1 = "jm2", username_2 = "js1"
                                                        ).first()
    
    # Deletes the created relationship from the database and saves its state
    db.session.delete(current_relationship)
    db.session.commit()

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
    db.drop_all()

    # Deletes the context object
    test_request_context.pop()


#******************
#***User Story D***
#******************

#*************
#***Test 10***
#*************
def test_valid_post_like():
    '''
    Ensures that a user can like another user's post.
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

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

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
        "account_identifier": "js1",
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
        db.session.commit()
        

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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "js1", username_2 = "jm2",
                                        relationship_type = RelationshipType.SENT_REQUEST
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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

    '''
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
    '''

    # Retrieves the relationship created between the user's "js1" and "jm2"
    current_relationship = Relationship.query.filter_by (
                                                            username_1 = "js1", username_2 = "jm2"
                                                        ).first()
    
    # Modifies the relationshipi between the user's "js1" and "jm2" and saves its state
    # The relationship is between the users is now "FRIEND"
    current_relationship.relationship_type = RelationshipType.FRIEND
    db.session.commit()

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

    # <TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; test case turning point begin
    
    '''
    url = '/share_post/' + str(new_post_id)

    # Shares a post from "js1" that should then appeat in "jm2's" timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    '''

    # Imports the database table "Share" from the file "app.py"
    from Code.app import Share

    # Manually creates a new post, circumventing the need to interface with a session variable
    new_share = Share(
      post_id = new_post_id, username = "jm2", 
      shared_time = datetime.now()
    )

    # Saves the shared post into the database
    db.session.add(new_share)
    db.session.commit()

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
    assert b"jm2" in response.data
    assert b"title=\"Likes\"> 0 </button>" in response.data

    '''
    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/modify_post_likes/' + str(new_post_id)

    # Shares a post from "js1" that should then appeat in "jm2's" timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    '''

    # Imports the database table "PostLikes" from the file "app.py"
    from Code.app import PostLikes

    # Manually likes a post, circumventing the need to interface with a session variable
    new_like = PostLikes(
          post_id = new_post_id, username = "jm2"
    )

    # Saves the state of the toggled like counter into the database
    db.session.add(new_like)
    db.session.commit()

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
    assert b"jm2" in response.data
    assert b"title=\"Likes\"> 1 </button>" in response.data

    # </TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; ; test case turning point end

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    db.drop_all()
    
    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 11***
#*************
def test_valid_post_share():
    '''
    Ensures that a user can share another user's post.
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

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

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
        "account_identifier": "js1",
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
        db.session.commit()
        

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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "js1", username_2 = "jm2",
                                        relationship_type = RelationshipType.SENT_REQUEST
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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

    '''
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
    '''

    # Retrieves the relationship created between the user's "js1" and "jm2"
    current_relationship = Relationship.query.filter_by (
                                                            username_1 = "js1", username_2 = "jm2"
                                                        ).first()
    
    # Modifies the relationshipi between the user's "js1" and "jm2" and saves its state
    # The relationship is between the users is now "FRIEND"
    current_relationship.relationship_type = RelationshipType.FRIEND
    db.session.commit()

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

    # <TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; test case turning point begin
    
    '''
    url = '/share_post/' + str(new_post_id)

    # Shares a post from "js1" that should then appeat in "jm2's" timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    '''

    # Imports the database table "Share" from the file "app.py"
    from Code.app import Share

    # Manually creates a new post, circumventing the need to interface with a session variable
    new_share = Share(
      post_id = new_post_id, username = "jm2", 
      shared_time = datetime.now()
    )

    # Saves the shared post into the database
    db.session.add(new_share)
    db.session.commit()

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
    assert b"jm2" in response.data

    # </TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; ; test case turning point end

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    db.drop_all()
    
    # Deletes the context object
    test_request_context.pop()

#*************
#***Test 12***
#*************
def test_valid_post_commenting():
    '''
    Ensures that a user can comment on another user's post.
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

    # Imports the database user table "User" and the instance of the bcrypt object initialized in the file "app.py"
    from Code.app import User, bcrypt

    # Creates a temporary user to interface with the web application
    user_1 = User   (
                        username = 'js1',
                        password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                        first_name = 'James',
                        middle_name = '',
                        last_name = 'Smith',
                        email = 'js1@gmail.com'
                    )
    user_2 = User   (
                    username = 'jm2',
                    password = bcrypt.generate_password_hash('aA1@sldkepwnwkf'),
                    first_name = 'Jane',
                    middle_name = '',
                    last_name = 'Meredith',
                    email = 'jm2@gmail.com'
                    )

    # Saves the newly created user into the database
    if (1):
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

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
        "account_identifier": "js1",
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
        db.session.commit()
        

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

    '''
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
    '''

    # Imports the database table "Relationship" and its helder class "RelationshipType"
    from Code.app import Relationship, RelationshipType

    # Creates a new relationship between the test users, "js1" and "jm2"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    new_relationship = Relationship (
                                        username_1 = "js1", username_2 = "jm2",
                                        relationship_type = RelationshipType.SENT_REQUEST
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()
    
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

    '''
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
    '''

    # Retrieves the relationship created between the user's "js1" and "jm2"
    current_relationship = Relationship.query.filter_by (
                                                            username_1 = "js1", username_2 = "jm2"
                                                        ).first()
    
    # Modifies the relationshipi between the user's "js1" and "jm2" and saves its state
    # The relationship is between the users is now "FRIEND"
    current_relationship.relationship_type = RelationshipType.FRIEND
    db.session.commit()

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

    # <TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; test case turning point begin
    
    '''
    url = '/submit_comment/' + str(new_post_id)
    data = {
        "comment_text": "lethologica",
    }

    response = app.test_client().post(url, data=data, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    '''

    # Imports the database table "Comment" from the file "app.py"
    from Code.app import Comment

    # Generates and populates the arguments passed to the Comment object constructor
    new_comment_id = randrange(pow(2, 31) - 1)
    new_comment_text = "lethologica"

    # Manually creates a new comment, circumventing the need to interface with a session variable
    new_comment = Comment(
      comment_id = new_comment_id, username = "jm2",
      parent_id = new_post_id,
      comment_text = new_comment_text,
      original_comment_time = datetime.now()
    )

    # Saves the comment into the database
    db.session.add(new_comment)
    db.session.commit()

    # Creates a new relationship between the test users, "jm2" and "js1"
    # Sets the relationship between the individuals as friends, meaning that have sent and accpeted a friend request respectively
    # Circumvents the need to modify a session whose value contains arguments
    # Such a circumstance arises when evoking the url "/modify_relationship/<username>"
    
    # A "Friend" relationship status is not bi-directional
    # This means that a "Friend" relationship exists between the users "js1" and "jm2" in that order
    # But the converse is not implicity set, which necessitates the following
    new_relationship = Relationship (
                                        username_1 = "jm2", username_2 = "js1",
                                        relationship_type = RelationshipType.FRIEND
                                    )

    # Saves the newly created relationship into the database
    db.session.add(new_relationship)
    db.session.commit()

    # Initializes a response object to automate testing
    # Build the arguments that will be passed to the response object
    url = '/user/' + str("js1") + '/timeline'

    # Loads the user's timeline
    response = app.test_client().get(url, follow_redirects=True)

    # A successfully loaded page should return a response status code of 200
    assert response.status_code == 200
    assert b"Test Post #1" in response.data
    assert b"js1" in response.data
    assert b"Username" in response.data
    assert b"Original Post Time" in response.data
    assert b"jm2" in response.data
    assert b"lethologica" in response.data

    # </TEST CASE TURNING POINT> : the following code will differ with each User Story D test case; ; test case turning point end

    # </TESTING PLACEHOLDER> : testing statements end

    # Cleans the database dropping its tables
    db.drop_all()
    
    # Deletes the context object
    test_request_context.pop()
