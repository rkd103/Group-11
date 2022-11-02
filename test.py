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
    db.drop_all()

    # Deletes the context object
    test_request_context.pop()
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
    flask_login.logout_user()

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
