#**********************
#***Library*Includes***
#**********************

from class_objects import Current_User
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from bcrypt_cryptographic_transformation import Credential, generate_hash, validate_hash
from rstr import Rstr, rstr, xeger
from random import SystemRandom
from flask_mail import Mail, Message
import base64

#******************************************
#***Function*Declarations*and*Defintions***
#******************************************
def generate_password():
    rstr = Rstr(SystemRandom())
    return (rstr.xeger(r'[0-9a-zA-Z]{15}[^a-zA-Z0-9\s:]{15}'))

# Source: https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/
def send_email(recipient_email, email_subject_line, email_content):
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cse.4212.group.11@gmail.com'
    app.config['MAIL_PASSWORD'] = base64.b64decode('amVvemZwaGxjdWthd3dtZQ==').decode("utf-8")

    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

    message = Message   (
                            email_subject_line,
                            sender='cse.4212.group.11@gmail.com',
                            recipients=[recipient_email]
                        )
    message.body = email_content

    mail.send(message)
    return ("Email Sent")


#**************************
#***Object*Instantiation***
#**************************

# Creates an instance of a Flask object
app = Flask(__name__)
# Creates the database extension
db = SQLAlchemy()
# Configures the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# Initializes the app with the extension
db.init_app(app)


#*********************
#***Database*Tables***
#*********************

class User(db.Model):
    username = db.Column(db.String(1024), unique=True, primary_key=True)
    salt = db.Column(db.String(1024), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    first_name = db.Column(db.String(1024), nullable=False)
    middle_name = db.Column(db.String(1024), nullable=True)
    last_name = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(1024), unique=True, nullable=False)


#****************************************
#***Web*Application*Pages*and*Routines***
#****************************************

# Adds functions to return content using Flask's decorator to map various URL routes to a given function

#*************************
#***Inital*Loading*Page***
#*************************
@app.route("/")
def home():
    # Creates a status indicator to indicate that an error has occurred during the account creation process
    # When the the status is (0), means that a popup shoud not render on the web application's homepage
    # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
    account_creation_flag = 0
    login_validation_flag = 0
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_status = 0
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_edge_case = 0
    return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)

#****************
#***Login*Page***
#****************
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Creates a user to modify in the python script
    current_user = Current_User(username=request.form['username'], password=request.form['password'])
    
    # Creates a status indicator to express the current state of the login validation process
    # When the status is (0), means that the provided credentials are valid
    # When the status is (1), means that the provided credentials are invalid
    login_validation_flag = 0

    # Validates the user's input agaisnt the database
    database_table_user = User.query.all()
    for database_user in database_table_user:
        if (database_user.username == current_user.username):
            if (validate_hash(salt=database_user.salt, password=current_user.password, hashed_password=database_user.password)):
                #Implement: Create skeleton for the user's account page
                return render_template('user_account.html')
            else:
                login_validation_flag = 1
                # When the the status 'account_creation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
                # Returns to the web application's homepage and print an error popup
                # When the status is (1), means that either the username was queried and returned to the user or they received a new password
                # When the status is (0), means that the fogot credential routine was not executed
                forgot_credential_routine_status = 0
                return render_template("home.html", account_creation_flag=0, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)
                
        else:
            login_validation_flag = 1
            # When the the status 'account_creation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
            # Returns to the web application's homepage and print an error popup
            # When the status is (0), means that the fogot credential routine was not executed
            forgot_credential_routine_status = 0
            # When the status is (0), means that the fogot credential routine was not executed
            forgot_credential_routine_edge_case = 0
            return render_template("home.html", account_creation_flag=0, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)

#*****************************
#***Forgot*Credentials*Page***
#*****************************
@app.route("/forgot_credentials")
def forgot_credentials():
    # Creates a status indicator to express when one of the input fields is incorrect
    # When the status is (1), means that an one of the fields for the forgot_credentials form is invalid
    # When the status is (0), means that the fields are valid
    forgot_credential_invalid_field_value_status = 0
    return render_template('forgot_credentials.html', forgot_credential_invalid_field_value_status=forgot_credential_invalid_field_value_status)

#*******************************************************
#***Forgot*Credentials*Page*--*Database*Search*Routine***
#*******************************************************
@app.route("/account_retrival", methods=['GET', 'POST'])
def account_retrival():
    # Creates a user to modify in the python script
    current_user = User(username=request.form['username'], password=request.form['password'], email=request.form['email'])

    # Creates a status indicator to express when one of the optional fields (username or password & email) are present
    # When the status is (1), means that the user provided their username
    # When the status is (0), means that the user provided their email and password
    optional_field_status = 1
    # Creates a status indicator that stores when the user has successfuly retrieved their username or generated a new password
    # When the status is (1), means that either the username was queried and returned to the user or they received a new password
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_status = 0
    # Creates a status indicator to indicate the following: the user completed every field presented during the forgot credential screen/form and correctly entered the required infomration for every field
    # When the status is (1), means that the user essentially logged in; rather, the user knows their credentials (given how they correctly entered them in for every optional field)
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_edge_case = 0
    
    # Conditionally checks whether the user provided their usersname or password and email
    if (current_user.username != "" and current_user.password != "" and current_user.email != ""):
        # Queries the database for the user table
        # Check whether the the credentials (username and email) exists in the database
        database_table_user = User.query.all()
        for database_user in database_table_user:
            if (current_user.email == database_user.email and current_user.username == database_user.username):
                # If the supplied username and email exist in the database, retrieve the user's salt and hashed password
                # Use the function 'validate_hash()' to determine whether the password associated with the furnisehd username and email is correct
                if (validate_hash(database_user.salt, current_user.password, database_user.password)):
                    #If everything is valid: redirct back to the hompage and display a popup indicating that the user knows their login credentials
                    # Creates a status indicator to indicate that an error has occurred during the account creation process
                    # When the the status is (0), means that a popup shoud not render on the web application's homepage
                    # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
                    account_creation_flag = 0
                    login_validation_flag = 0
                    # Return the user's username if both the email existed and the password was valid
                    # Redirct back to the hompage and display a warning popup
                    # When the status is (0), means that the fogot credential routine was not executed
                    forgot_credential_routine_status = 0
                    # When the status is (1), means that the user essentially logged in; rather, the user knows their credentials (given how they correctly entered them in for every optional field)
                    forgot_credential_routine_edge_case = 1
                    return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case) 
    if (current_user.username != ""):
        # When the status is (1), means that the user provided their username
        optional_field_status = 1

        # Queries the database for the user table
        # Searches the user table for the provided username
        database_table_user = User.query.all()
        for database_user in database_table_user:
            if (current_user.username == database_user.username):
                # Generates a password
                current_user.password = generate_password()
                
                # Stores the generated password to send to the user's email
                temporary_password = current_user.password

                # Uses the function 'generate_hash()' to produce a new salt and ciphertext
                temporary_credentials = generate_hash(current_user.password)
                # Stores the newly produced salt and ciphertext into the database
                database_user.salt = temporary_credentials.salt
                database_user.password = temporary_credentials.hashed_password

                # Commits changes to database
                db.session.commit()

                # Send the user an email with the temporary, non-ciphertext password
                msg =  """
Hello %s:


We received a request to reset your password for your Hand-in-Hand account: %s.

Your new password is: 

"%s"

Please reaccess your account and join hand-in-hand with your friends and loved ones!


Best Regards,

The Hand-in-Hand™ Development Team
Contact: cse.4212.group.11@gmail.com
""" % (database_user.first_name, database_user.username, temporary_password)
                send_email(recipient_email=database_user.email, email_subject_line='Hand-in-Hand™ Credential Retrival/Reset Routine', email_content=msg)
                # Creates a status indicator to indicate that an error has occurred during the account creation process
                # When the the status is (0), means that a popup shoud not render on the web application's homepage
                # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
                account_creation_flag = 0
                login_validation_flag = 0
                # Redirct back to the hompage and display a popup indicating that an email was sent containing their newly generated password
                # When the status is (1), means that either the username was queried and returned to the user or they received a new password
                forgot_credential_routine_status = 1
                return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)

    if (current_user.password != "" and current_user.email != ""):
        # When the status is (0), means that the user provided their email and password
        optional_field_status = 0
        
        # Queries the database for the user table
        # Searches the database for the supplied email and retrieves the user's salt and hashed password
        database_table_user = User.query.all()
        for database_user in database_table_user:
            if (current_user.email == database_user.email):
                # Checks whether the provided password matches with the one associated with furnished email
                # Use the function 'validate_hash()' to determine whether the provided password is correct
                if (validate_hash(database_user.salt, current_user.password, database_user.password)):
                    # Send the user an email with their username
                    msg =  """
Hello %s:


We received a request to retrieve the username for your Hand-in-Hand account: %s.

Your username is: 

"%s"

Please reaccess your account and join hand-in-hand with your friends and loved ones!


Best Regards,

The Hand-in-Hand™ Development Team
Contact: cse.4212.group.11@gmail.com
""" % (database_user.first_name, database_user.email, database_user.username)
                send_email(recipient_email=database_user.email, email_subject_line='Hand-in-Hand™ Credential Retrival/Reset Routine', email_content=msg)
                # Creates a status indicator to indicate that an error has occurred during the account creation process
                # When the the status is (0), means that a popup shoud not render on the web application's homepage
                # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
                account_creation_flag = 0
                login_validation_flag = 0
                # Return the user's username if both the email existed and the password was valid
                # Redirct back to the hompage and display a popup indicating that an email was sent containing their username
                # When the status is (1), means that either the username was queried and returned to the user or they received a new password
                forgot_credential_routine_status = 1
                return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)

    # If some field is invalid, redirect back to the forgot credentials pageforgot_credential_invalid_field_value_status
    # When the status is (1), means that an one of the fields for the forgot_credentials form is invalid
    forgot_credential_invalid_field_value_status = 1
    return render_template('forgot_credentials.html', forgot_credential_invalid_field_value_status=forgot_credential_invalid_field_value_status)

#***************************
#***Account*Creation*Page***
#***************************
@app.route("/create_account")
def create_account():
    # Creates a status indicator to express when the second password field does not match the original
    # When the status is (0), means that the password fields match (or that the account creation process has not been initiated)
    password_input_flag = 0
    # Creates a status indicator to express when user's provided email and/or username conficts (or already exists) in the database
    # When the status is (0), means that both fields are unique
    uniqueness_flag = 0
    return render_template('create_account.html', password_input_flag=password_input_flag, uniqueness_flag=uniqueness_flag)

#***********************************************
#***Account*Creation*Page*--*Input*Validation***
#***********************************************
@app.route("/validate_credentials", methods=['GET', 'POST'])
def validate_credentials():
    # Creates a user to modify in the python script
    current_user = Current_User(username=request.form['username'], password=request.form['password'], first_name=request.form['first_name'], middle_name=request.form['middle_name'], last_name=request.form['last_name'], email=request.form['email'], password_confirmation=request.form['password_confirmation'])

    # Creates a status indicator to indicate that an error has occurred during the account creation process
    # When the the status is (1), means that a popup shoud render on the web application's homepage
    account_creation_flag = 1
    # Creates a status indicator to express when the second password field does not match the original
    # When the status is (0), means that the password fields match (or that the account creation process has not been initiated)
    password_input_flag = 0
    # Creates a status indicator to express when user's provided email and/or username conficts (or already exists) in the database
    # When the status is (0), means that both fields are unique
    # When the statis is (1), means one or more of the fields are not unique
    uniqueness_flag = 0
    if(current_user.password != current_user.password_confirmation):
        # When the status is (1), means that the passwords fields do not match
        # Conditionally alters the webpage to indicate the error
        password_input_flag = 1
        # Creates a status indicator to express when user's provided email and/or username conficts (or already exists) in the database
        # When the status is (0), means that both fields are unique
        return render_template("create_account.html", password_input_flag=password_input_flag, uniqueness_flag=uniqueness_flag)
    else:
        # Takes the users password and generates ciphertext and salt
        password_security_object = generate_hash(password=current_user.password)
        current_user.password = password_security_object.hashed_password
        current_user.salt = password_security_object.salt

        # Error checking
        try:
            # Creates a user to add to the database
            database_user_instance = User( username=current_user.username, 
                            salt=current_user.salt, 
                            password=current_user.password, 
                            first_name=current_user.first_name, 
                            middle_name=current_user.middle_name, 
                            last_name=current_user.last_name, 
                            email=current_user.email)
            # Adds the user to the database
            db.session.add(database_user_instance)

            # Commits changes to the database
            db.session.commit()
        except (exc.IntegrityError):
            # When the status is (0), means that the password fields match (or that the account creation process has not been initiated)
            # Creates a status indicator to express when user's provided email and/or username conficts (or already exists) in the database
            # When the statis is (1), means one or more of the fields are not unique
            uniqueness_flag = 1
            # Renders the following message on the account creation screen and makes certain borders red: "The selected username has already been claimed and/or the provided email has already been registered. Please modify one or more of the aforementioned fields.""
            return render_template('create_account.html', password_input_flag=password_input_flag, uniqueness_flag=uniqueness_flag)
        
        # Uses template to render HTML webpage
        # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
        login_validation_flag = 0
        # When the status is (0), means that the fogot credential routine was not executed
        forgot_credential_routine_status = 0
        # When the status is (0), means that the fogot credential routine was not executed
        forgot_credential_routine_edge_case = 0
        return render_template('home.html', account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, forgot_credential_routine_edge_case=forgot_credential_routine_edge_case)


#*****************
#***Driver*code***
#*****************

if __name__ == "__main__":
    # Creates the initial database
    # Sets up the application's context to create the database's tables
    with app.app_context():
        db.create_all()
    # Specifies the localhost
    app.run(host='0.0.0.0', )