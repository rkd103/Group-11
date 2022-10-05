#**********************
#***Library*Includes***
#**********************

from requests import post
from class_objects import Current_User
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from bcrypt_cryptographic_transformation import Credential, generate_hash, validate_hash
from rstr import Rstr, rstr, xeger
from random import SystemRandom, randrange, seed
from flask_mail import Mail, Message
import base64
from datetime import datetime
import enum

#**********************
#***Global*Variables***
#**********************
# Initializes a count to store the number of login attempts
login_attempts = 20
# Initializes a list to store the emails or usernames that the user passed into the login prompt
# The program will iterate through the list, changing the password of every valid username or email, effectively locking the user out of their account
# This is a poor implementation given that a bad actor could uncover their target's email, and lock them out of their account
invalid_credential_list = []

#******************************************
#***Function*Declarations*and*Defintions***
#******************************************
def generate_password():
    rstr = Rstr(SystemRandom())
    return (rstr.xeger(r'[a-zA-z0-9]{7}[0-9]{1}[^a-zA-z0-9\n\t\r\s]{7}'))

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
#********************~******

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
    login_status = db.Column(db.Boolean, default=False, nullable=False)
    # Should store a URL to some cloud storage receptecle
    profile_picture = db.Column(db.String(1024), nullable=True)
    # Should store a URL to some cloud storage receptecle
    background_banner_image = db.Column(db.String(1024), nullable=True)
    user_description = db.Column(db.String(1024), nullable=True)
    objective = db.Column(db.String(1024), nullable=True)
    phone_number = db.Column(db.String(9), nullable=True)

# username_1 and username_2 based on alphabetical order
# username_1 (relationship) username_2
# No row in table -> no relationship
class RelationshipType(enum.Enum):
    SENT_REQUEST = 1
    RECEIVED_REQUEST = 2
    FRIEND = 3
class Relationship(db.Model):
    username_1 = db.Column(db.String(1024), primary_key=True)
    username_2 = db.Column(db.String(1024), primary_key=True) 
    relationship_type = db.Column(db.Enum(RelationshipType))

class Post(db.Model):
    post_id = db.Column(db.Integer, unique=True, primary_key=True)
    username = db.Column(db.String(1024), nullable=False)
    post_text = db.Column(db.String(1024), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    num_shares = db.Column(db.Integer, nullable=False)
    num_comments = db.Column(db.Integer, nullable=False)
    original_post_time = db.Column(db.TIMESTAMP, nullable=False)
    last_edit_time = db.Column(db.TIMESTAMP, nullable=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.String(1024), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    original_comment_time = db.Column(db.TIMESTAMP, nullable=False)
    last_edit_time = db.Column(db.TIMESTAMP, nullable=True)

class Share(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username_receiver = db.Column(db.String(1024), nullable=False, primary_key=True)
    username_sender = db.Column(db.String(1024), nullable=False, primary_key=True)
    shared_time = db.Column(db.String(1024), nullable=False)

class PostLikes(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

class CommentLikes(db.Model):
    comment_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

#****************************************
#***Web*Application*Pages*and*Routines***
#****************************************

# Adds functions to return content using Flask's decorator to map various URL routes to a given function

#*************************
#***Inital*Loading*Page***
#*************************
@app.route("/")
def home():
    # Implicitly logs out every user
    # Works under the assumption that if the web application sends the user back to the homepage, they have finished their session with the website
    database_table_user = User.query.all()
    for database_user in database_table_user:
        database_user.login_status = 0
        db.session.commit()

    # Uses the global identifer to reference to the similarly named variable outside the scope of the function
    global login_attempts

    # Creates a status indicator to indicate that an error has occurred during the account creation process
    # When the the status 'account_creation_flag' is (0), means that a popup shoud not render on the web application's homepage
    # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
    account_creation_flag = 0
    login_validation_flag = 0
    # Creates a status indicator to indicate that the user has exceeded the permissible amount of login attempts
    # When the status 'disabled_account_status' is (0), means that a popup should not render on the web application's homepage
    # When the status 'disabled_account_status' is (1), means that a popup should render on the web application's homepage
    disabled_account_status = 0
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_status = 0

    return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, disabled_account_status=disabled_account_status)

#****************
#***Login*Page***
#****************
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Uses the global identifer to reference to the similarly named variable outside the scope of the function
    global login_attempts
    global invalid_credential_list

    # Creates a user to modify in the python script
    current_user = Current_User(username=request.form['username/email'], password=request.form['password'], email=request.form['username/email'])
    
    # Creates a status indicator to express the current state of the login validation process
    # When the status is (0), means that the provided credentials are valid
    # When the status is (1), means that the provided credentials are invalid
    login_validation_flag = 0

    # Validates the user's input agaisnt the database
    database_table_user = User.query.all()
    for database_user in database_table_user:
        if (database_user.username == current_user.username or database_user.email == current_user.email):
            if (validate_hash(salt=database_user.salt, password=current_user.password, hashed_password=database_user.password)):
                # Switches the status of the login_status flag, indicating that the current user is signed into the system
                database_user.login_status = 1
                # Finalize changes to the database
                db.session.commit()

                # Uses an templated skeleton to render the user's account
                return redirect(url_for('user_timeline'))

    
    # Increments counter for the permissable number of logins
    login_attempts -= 1
    # Stores the potentially valid credentials (username and/or email) in a list to iterate through later
    invalid_credential_list.append(request.form['username/email'])
    # Checks whether the number of attempts is greater than 20
    if (login_attempts == 0):
        login_attempts = 20
        # Queries the database for the user table
        database_table_user = User.query.all()
        # Iterates through the list of invalid credentials, replacing the passwords tied to the user's suspected username and email
        # A generated password is substituted for the original password, effectively locking the user out of their account
        # This is an exploitable feature, but if a user's account is wrongfully locked, they can reaccess their account using the forgot credential avenue
        for username_or_email in invalid_credential_list:
            for database_user in database_table_user:
                if (username_or_email == database_user.email or username_or_email == database_user.username):
                    new_password = generate_password()
                    new_credentials = generate_hash(password=new_password)
                    database_user.password = new_credentials.hashed_password
                    database_user.salt = new_credentials.salt
                    # Commits changes to the database
                    db.session.commit()
        
        # When the the status 'account_creation_flag' is (0), means that a popup shoud not render on the web application's homepage
        account_creation_flag = 0
        # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
        login_validation_flag = 0
        # When the status 'disabled_account_status' is (0), means that a popup should not render on the web application's homepage
        disabled_account_status = 0
        # When the status 'disabled_account_status' is (1), means that a popup should render on the web application's homepage
        disabled_account_status = 1
        # When the status is (0), means that the fogot credential routine was not executed
        forgot_credential_routine_status = 0

        # Prints out a popup message indicating that the user is now locked out of their account indefintiely
        # By "locked out," we mean that the user's password has ben changed and the user has not way of knowing what the new password is
        return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, disabled_account_status=disabled_account_status)

    # Captures an edge case when the database is empty, meaning that querying the databse returned nothing or 'None'
    # In such cases, the function drops through or disregards the conditional checks
    login_validation_flag = 1
    # When the the status 'account_creation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
    # Returns to the web application's homepage and print an error popup
    # When the status is (1), means that either the username was queried and returned to the user or they received a new password
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_status = 0
    return render_template("home.html", account_creation_flag=0, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status, login_attempts=login_attempts)

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
    current_user = User(email=request.form['email'])

    # Creates a status indicator to express when one of the optional fields (username or password & email) are present
    # When the status is (1), means that the user provided their username
    # When the status is (0), means that the user provided their email and password
    optional_field_status = 1
    # Creates a status indicator that stores when the user has successfuly retrieved their username or generated a new password
    # When the status is (1), means that either the username was queried and returned to the user or they received a new password
    # When the status is (0), means that the fogot credential routine was not executed
    forgot_credential_routine_status = 0
    
    # Conditionally checks whether the user provided their email
    if (current_user.email != ""):
        # Queries the database for the user table
        # Check whether the the credentials (or email) exists in the database
        database_table_user = User.query.all()
        for database_user in database_table_user:
            if (current_user.email == database_user.email):
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


We received a request to reset the password associated with the following account: %s.

Your new password is: 

"%s"

Please reaccess your account and join "hand-in-hand" with your friends and loved ones!


Best Regards,

The Hand-in-Hand™ Development Team
Contact: cse.4212.group.11@gmail.com
""" % (database_user.first_name, database_user.email, temporary_password)
                send_email(recipient_email=database_user.email, email_subject_line='Hand-in-Hand™ Credential Reset Routine', email_content=msg)
                # Creates a status indicator to indicate that an error has occurred during the account creation process
                # When the the status 'account_creation_flag' is (0), means that a popup shoud not render on the web application's homepage
                # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
                account_creation_flag = 0
                login_validation_flag = 0
                # Redirct back to the hompage and display a popup indicating that an email was sent containing their newly generated password
                # When the status is (1), means that either the username was queried and returned to the user or they received a new password
                forgot_credential_routine_status = 1
                return render_template("home.html", account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status)

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
        
        # Send the user an email with a notification of their account creation
        msg =  """
Hello %s:


Thank you for registering at Hand-in-Hand.

To access your account, please click on the following link or copy-paste it into your browser: http://127.0.0.1:5000/.


Best Regards,

The Hand-in-Hand™ Development Team
Contact: cse.4212.group.11@gmail.com
""" % (current_user.first_name)
        send_email(recipient_email=current_user.email, email_subject_line='Welcome to Hand-in-Hand™ %s!' % current_user.first_name, email_content=msg)

        # Uses template to render HTML webpage
        # When the the status 'login_validation_flag' is (0), means that a popup related to the status shoud not render on the web application's homepage
        login_validation_flag = 0
        # When the status is (0), means that the fogot credential routine was not executed
        forgot_credential_routine_status = 0
        return render_template('home.html', account_creation_flag=account_creation_flag, login_validation_flag=login_validation_flag, forgot_credential_routine_status=forgot_credential_routine_status)

#***********************
#***Account*retrieval***
#***********************
def get_current_user():
    return User.query.filter_by(login_status = 1).first()

#**************************
#***User's*timeline*page***
#**************************
@app.route('/home/timeline', methods=['GET', 'POST'])
def user_timeline():
    current_user = get_current_user()
    if (current_user == None):
        redirect(url_for('login'))

    # Get personal posts and order by timestamp
    user_timeline = Post.query.filter_by(username = current_user.username)
    user_timeline = user_timeline.order_by(Post.original_post_time.desc())
    user_timeline = user_timeline.all()

    # TODO: Get shared posts and order with user posts

    return render_template('personal_timeline.html', timeline = user_timeline)

#***********************
#***Submit*a*new*post***
#***********************
@app.route('/home/timeline/submit_post', methods=['GET', 'POST'])
def submit_post():
    current_user = get_current_user()
    if current_user == None:
        raise Exception('Error in submitting post')

    # Generate unique post id
    seed = datetime.now()
    new_post_id = randrange(pow(2, 31) - 1)
    if Post.query.filter_by(post_id = new_post_id).first() != None:
        seed = datetime.now()
        new_post_id = randrange(pow(2, 31) - 1)

    new_post = Post(
        post_id = new_post_id,
        username = current_user.username,
        post_text = request.form.get('post_text'),
        num_likes = 0,
        num_shares = 0,
        num_comments = 0,
        original_post_time = datetime.now(),
        last_edit_time = None
    )

    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for('user_timeline'))

#*******************
#***Delete*a*post***
#*******************
@app.route('/home/timeline/delete_post/<post_to_delete_id>')
def delete_post(post_to_delete_id):
    post_database_table = Post.query.all()
    for post in post_database_table:
        if (post.post_id == int(post_to_delete_id)):
            db.session.delete(post)
            db.session.commit()
    return redirect(url_for('user_timeline'))

#*************************
#***User's*friends*page***
#*************************
@app.route('/home/friends')
def user_friends():
    current_user = get_current_user()
    if (current_user == None):
        redirect(url_for('login'))
    return render_template('friends.html')

#*************************
#***User's*account*page***
#*************************
@app.route('/home/account')
def user_account():
    current_user = get_current_user()
    if (current_user == None):
        redirect(url_for('login'))
    return render_template('account.html')

#***********************
#***Logout*of*Account***
#***********************
@app.route('/home/logout')
def logout():
    return render_template('home.html')


#*****************
#***Driver*code***
#*****************
if __name__ == "__main__":
    # Creates the initial database
    # Sets up the application's context to create the database's tables
    with app.app_context():
        # Uncomment to clear the database
        # db.drop_all()      
        db.create_all()
    # Specifies the localhost
    app.run(host='0.0.0.0', )