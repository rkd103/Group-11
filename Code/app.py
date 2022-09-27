#**********************
#***Library*Includes***
#**********************

from class_objects import Current_User
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from bcrypt_cryptographic_transformation import Credential, generate_hash, validate_hash
import rstr
from rstr import digits


#******************************************
#***Function*Declarations*and*Defintions***
#******************************************
def generate_password():
    return (rstr.xeger(r'[\da-zA-Z\W\D]{15}'))


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
    return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag)

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
                return render_template("home.html", account_creation_flag=0, login_validation_flag=login_validation_flag)
                
        else:
            login_validation_flag = 1
            # When the the status 'account_creation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
            # Returns to the web application's homepage and print an error popup
            return render_template("home.html", account_creation_flag=0, login_validation_flag=login_validation_flag)

#*****************************
#***Forgot*Credentials*Page***
#*****************************
@app.route("/forgot_credentials")
def forgot_credentials():
    return render_template('forgot_credentials.html')

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
    
    # Conditionally checks whether the user provided their usersname or password and email
    if (current_user.username != ""):
        # When the status is (1), means that the user provided their username
        optional_field_status = 1

        # Queries the database for the user table
        # Searches the user table for the provided username
        database_table_user = User.query.all()
        for database_user in database_table_user:
            if (current_user.username == database_user.username):
                current_user.password = generate_password()
                
                temporary_password = current_user.password

                temporary_credentials = generate_hash(current_user.password)
                database_user.salt = temporary_credentials.salt
                database_user.password = temporary_credentials.hashed_password

        #Implement: search the database for the username
            #Implement: generate a password
            #Implement: use the function 'generate_hash()' to produce a new salt and ciphertext
            #Implement: store new salt and ciphertext in the database
            #Implement: send the user an email with the temporary, non-ciphertext password
            #Implement: redirct back to the hompage and display a popup indicating that an email was sent containing their newly generated password
        None
    if (current_user.password != "" and current_user.email != ""):
        # When the status is (0), means that the user provided their email and password
        optional_field_status = 0
        #Implement: search the database for the email and retrieve the user's salt and hashed password
        #Implement: use the function 'validate_hash()' to determine whether the password is correct
        #Implement: return the user's username if both the email existed and the password was valid
        None
    if (current_user.username != "" and current_user.password != "" and current_user.email != ""):
        #Implement: check whether the the credentials (username and email) exists in the database
        #Implement: if the username and email exist in the daabase, retrieve the user's salt and hashed password
        #Implement: use the function 'validate_hash()' to determine whether the password is correct
        #Implement: if everything is valid: redirct back to the hompage and display a popup indicating that the user knows their login credentials
        #Implement: if something is invalid: redirect back to the forgot credentials page
        None
    return render_template('account_retrival.html', username=current_user.username, password=current_user.password, email=current_user.email, optional_field_status=optional_field_status)

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
        return render_template('home.html', account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag)


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