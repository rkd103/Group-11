#**********************
#***Library*Includes***
#**********************
from requests import post
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from rstr import Rstr, rstr, xeger
from random import SystemRandom, randrange
from flask_mail import Mail, Message
import base64
from datetime import datetime
import enum
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FileField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from wtforms_validators import Alpha
import os
from werkzeug.utils import secure_filename


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


#********************************************
#***Object*Instantiation*and*Configuration***
#********************************************

# Creates an instance of a Flask object
app = Flask(__name__)
# Creates the database extension
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# Configures the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET_KEY'] = 'T@&5RcGyBwXbVjb^%VX3'
UPLOADS = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOADS
app.config['ALLOWED_MEDIA_EXTENSIONS'] = ["PNG", "JPEG", "JPG", "GIF", "MP4", "MOV", "MKV"]
app.config['MAX_CONTENT_LENGTH'] = (10 * 1024 * 1024)

# Source: https://www.youtube.com/watch?v=6WruncSoCdI
def allowed_media(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_MEDIA_EXTENSIONS']:
        return True
    else:
        return False

# Source: https://stackoverflow.com/questions/19459236/how-to-handle-413-request-entity-too-large-in-python-flask-server
@app.errorhandler(413)
def request_entity_too_large(error):
    flash('That file is too large.\n\nIt exceeded the maximum size of 10MB.')
    return redirect(url_for('user_timeline'))

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def user_loader(username):
    return User.query.get(username)

#*********************
#***Database*Tables***
#*********************

class User(db.Model, UserMixin):
    username = db.Column(db.String(1024), primary_key=True)
    password = db.Column(db.String(1024), nullable=False)
    first_name = db.Column(db.String(1024), nullable=False)
    middle_name = db.Column(db.String(1024), nullable=True)
    last_name = db.Column(db.String(1024), nullable=False)
    email = db.Column(db.String(1024), unique=True, nullable=False)
    profile_picture = db.Column(db.String(1024), nullable=True)
    background_banner_image = db.Column(db.String(1024), nullable=True)
    user_description = db.Column(db.String(1024), nullable=True)
    objective = db.Column(db.String(1024), nullable=True)
    phone_number = db.Column(db.String(9), nullable=True)

    def get_id(self):
        return self.username

# username_1 < username_2
# username_1 (relationship) username_2
# No row in table -> no relationship
class RelationshipType(enum.Enum):
    NO_RELATIONSHIP = 0 # Used for backend purposes, not stored in db
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
    post_media = db.Column(db.String(1024), nullable=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.String(1024), nullable=False)
    num_likes = db.Column(db.Integer, nullable=False)
    original_comment_time = db.Column(db.TIMESTAMP, nullable=False)
    last_edit_time = db.Column(db.TIMESTAMP, nullable=True)

class Repost(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)
    repost_time = db.Column(db.TIMESTAMP, nullable=False)

class PostLikes(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

class CommentLikes(db.Model):
    comment_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

#*****************
#***Flask*Forms***
#*****************

class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(),
        Length(min=1, max=1024)
    ])
    first_name = StringField(validators=[
        InputRequired(),
        Length(min=1, max=1024),
        Alpha('First name should only contain letters.')
    ])
    middle_name = StringField(validators=[
        Length(max=1024)
    ])
    last_name = StringField(validators=[
        InputRequired(),
        Length(min=1, max=1024),
        Alpha('Last name should only contain letters.')
    ])
    email = EmailField(validators=[
        InputRequired(),
        Length(min=1, max=1024),
    ])
    password = PasswordField(validators=[
        InputRequired(),
        Length(min=15, max=1024)
    ])
    password_confirmation = PasswordField(validators=[
        InputRequired(),
        EqualTo('password', 'Passwords do not match.')
    ])
    submit = SubmitField('Sign Up')
    
    def validate_middle_name(self, middle_name):
        for char in middle_name.data:
            if not char.isalpha():
                raise ValidationError('Middle name should only contain letters')

    def validate_password(self, password):
        has_digit = False
        has_capital_letter = False
        has_lowercase_letter = False
        has_special_character = False

        for char in password.data:
            if char.isdigit():
                has_digit = True
                continue
            if char.isupper():
                has_capital_letter = True
                continue
            if char.islower():
                has_lowercase_letter = True
                continue
            if not char.isspace():
                has_special_character = True
                continue
            raise ValidationError('Password cannot contain whitespace')
        
        if not (has_digit and has_capital_letter and has_lowercase_letter 
        and has_special_character):
            error_message = 'Passwords must contain all of the following: ' + \
                '(1) a lowercase letter (a-z), ' + \
                '(2) a capital letter (A-Z), ' + \
                '(3) a digit (0-9), ' + \
                '(4) a special character (!@#%$^&*...)'
            raise ValidationError(error_message)

    def validate_username(self, username):
        # Prevent email from being used as username
        if username.data.find('@') != -1:
            raise ValidationError('Username cannot contain @.')
        # Check for unique username
        is_existing_user = User.query.filter_by(username = username.data).first()
        if is_existing_user:
            raise ValidationError('An account with that username already exists.')

    def validate_email(self, email):
        # Check for unique email
        is_existing_user = User.query.filter_by(email = email.data).first()
        if is_existing_user:
            raise ValidationError('An account with that email already exists.')

class LoginForm(FlaskForm):
    account_identifier = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField('Login')

#****************************************
#***Web*Application*Pages*and*Routines***
#****************************************

# Adds functions to return content using Flask's decorator to map various URL routes to a given function

#*************************
#***Inital*Loading*Page***
#*************************
@app.route("/")
def home():
    # Uses the session variable to create a count to keep track of the number of login attempts
    session['login_attempt'] = 20

    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('user_timeline'))

#****************
#***Login*Page***
#****************
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You must be logged out to access that page.')
        return redirect(url_for('user_timeline'))

    login_form = LoginForm()

    # Check login info
    if login_form.validate_on_submit():
        # Check username + password against database
        user = User.query.filter_by(username = login_form.account_identifier.data).first()
        if user != None:
            try:
                is_correct_password = bcrypt.check_password_hash(
                    pw_hash = user.password, 
                    password = login_form.password.data
                )
                if is_correct_password:
                    login_user(user, remember=False)
                    login_attempt = session.get('login_attempt')
                    login_attempt = 20
                    session['login_attempt'] = login_attempt
                    return redirect(url_for('user_timeline'))
            except (ValueError):
                None

            # Source: https://splunktool.com/counting-login-attempts-in-flask
            # Retrieves the session variable 'login_attempt,' decrements it, and updates the original value
            login_attempt = session.get('login_attempt')
            login_attempt -= 1
            session['login_attempt'] = login_attempt
            # Displays an error message to the user indicating the number of remaining attempts
            if login_attempt == 1:
                flash('This is your last attempt, Attempt %d of 20. ' % login_attempt, 'error')
                return redirect(url_for('login'))
            elif login_attempt < 20 and login_attempt > 1:
                flash('Invalid login credentials, Attempts %d of 20.' % login_attempt, 'error')
                return redirect(url_for('login'))
            else:
                flash('We\'ve detected suspicious activity on your Hand-in-Hand account and have temporarily locked it as a security precaution.\n\nIt\'s likely that your email was compromised as a result of phishing or other malicious means.\n\nIf you suspect that your account was wrongfully disabled, use the \"Forgot Credential\" option presented on the login screen.', 'error')
                user.password = generate_password()
                db.session.commit()
                login_attempt = session.get('login_attempt')
                login_attempt = 20
                session['login_attempt'] = login_attempt
                return redirect(url_for('login'))

        
        # Check email + password against database 
        user = User.query.filter_by(email = login_form.account_identifier.data).first()
        if user != None:
            try:
                is_correct_password = bcrypt.check_password_hash(
                    pw_hash = user.password, 
                    password = login_form.password.data
                )
                if is_correct_password:
                    login_user(user, remember=False)
                    login_attempt = session.get('login_attempt')
                    login_attempt = 20
                    session['login_attempt'] = login_attempt
                    return redirect(url_for('user_timeline'))
            except (ValueError):
                None

            # Source: https://splunktool.com/counting-login-attempts-in-flask
            # Retrieves the session variable 'login_attempt,' decrements it, and updates the original value
            login_attempt = session.get('login_attempt')
            login_attempt -= 1
            session['login_attempt'] = login_attempt
            # Displays an error message to the user indicating the number of remaining attempts
            if login_attempt == 1:
                flash('This is your last attempt, Attempt %d of 20. ' % login_attempt, 'error')
                return redirect(url_for('login'))
            elif login_attempt < 20 and login_attempt > 1:
                flash('Invalid login credentials, Attempts %d of 20.' % login_attempt, 'error')
                return redirect(url_for('login'))
            else:
                flash('We\'ve detected suspicious activity on your Hand-in-Hand account and have temporarily locked it as a security precaution.\n\nIt\'s likely that your email was compromised as a result of phishing or other malicious means.\n\nIf you suspect that your account was wrongfully disabled, use the \"Forgot Credential\" option presented on the login screen.', 'error')
                user.password = generate_password()
                db.session.commit()
                login_attempt = session.get('login_attempt')
                login_attempt = 20
                session['login_attempt'] = login_attempt
                return redirect(url_for('login'))

        flash('Invalid login credentials.')

    return render_template('login.html', login_form=login_form)

#*****************************
#***Forgot*Credentials*Page***
#*****************************
@app.route("/forgot_credentials")
def forgot_credentials():
    if current_user.is_authenticated:
        flash('You must be logged out to access that page.')
        return redirect(url_for('user_timeline'))

    return render_template('forgot_credentials.html')

#********************************************************
#***Forgot*Credentials*Page*--*Database*Search*Routine***
#********************************************************
@app.route("/account_retrieval", methods=['GET', 'POST'])
def account_retrieval():
    if current_user.is_authenticated:
        flash('You must be logged out to access that page.')
        return redirect(url_for('user_timeline'))

    try:
        user = User.query.filter_by(email = request.form.get('email')).first()
        if user == None:
            flash('There is no account tied to the provided email.')
            return redirect(url_for('forgot_credentials'))
    except: # Table hasn't been created yet
            flash('There is no account tied to the provided email.')
            return redirect(url_for('forgot_credentials'))
    
    # Generate new password for user
    temp_password = generate_password()
    temp_hashed_password = bcrypt.generate_password_hash(temp_password)
    user.password = temp_hashed_password
    db.session.commit()

    # Send the user an email with the temporary, non-ciphertext password
    f = open('reset_password_email.txt', 'r')
    msg = f.read()
    msg = msg.replace('first_name', user.first_name)
    msg = msg.replace('email', user.email)
    msg = msg.replace('new_password', temp_password)
    f.close()

    send_email(
        recipient_email = request.form.get('email'),
        email_subject_line = 'Hand-in-Hand™ Credential Reset Routine', 
        email_content = msg
    )

    flash('A temporary password has been sent to your email.')
    return redirect(url_for('login'))

#*******************************
#***Account*Registration*Page***
#*******************************
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You must be logged out to access that page.')
        return redirect(url_for('user_timeline'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Add new user to database
        new_user = User(
            username = register_form.username.data,
            password = bcrypt.generate_password_hash(register_form.password.data),
            first_name = register_form.first_name.data,
            middle_name = register_form.middle_name.data,
            last_name = register_form.last_name.data,
            email = register_form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        logout_user() # Prevent automatic login

        # Send email indicating successful account creation
        f = open('account_creation_email.txt', 'r')
        msg = f.read()
        msg = msg.replace('first_name', new_user.first_name)
        f.close()
        send_email(
            recipient_email = new_user.email,
            email_subject_line = 'Welcome to Hand-in-Hand™ %s!' % new_user.first_name,
            email_content = msg
        )

        flash('Welcome to Hand-in-Hand! Login to access your account.')
        return redirect(url_for('login'))

    return render_template('register.html', register_form=register_form)

#**************************
#***User's*timeline*page***
#**************************
@app.route('/home/timeline', methods=['GET', 'POST'])
@login_required
def user_timeline():
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()

    user_timeline = Post.query.filter_by(username = current_user.username)
    user_timeline = user_timeline.order_by(Post.original_post_time.desc()).all()

    # TODO: Reorder with reposts

    return render_template('personal_timeline.html', timeline = user_timeline, user = queried_user)

#***********************
#***Submit*a*new*post***
#***********************
@app.route('/home/timeline/submit_post', methods=['GET', 'POST'])
@login_required
def submit_post():      
    # Generate unique post id
    new_post_id = randrange(pow(2, 31) - 1)
    if Post.query.filter_by(post_id = new_post_id).first() != None:
        new_post_id = randrange(pow(2, 31) - 1)

    new_post = Post(
      post_id = new_post_id,
      username = current_user.username,
      post_text = request.form.get('post_text'),
      num_likes = 0,
      num_shares = 0,
      num_comments = 0,
      original_post_time = datetime.now(),
      last_edit_time = None,
      post_media = ""
    )

    # Reads in the media attached to a post
    # Source: https://www.youtube.com/watch?v=6WruncSoCdI
    if request.method == "POST":
        if request.files:

            media = request.files['media']

            if not media.filename == "":
                if allowed_media(media.filename):
                    filename = secure_filename(media.filename)
                    media.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                    new_post.post_media = filename
                    
                    db.session.add(new_post)
                else:
                    flash('That file extension is not allowed.')
            else:
                db.session.add(new_post)

    db.session.commit()

    return redirect(url_for('user_timeline'))

#*******************
#***Delete*a*post***
#*******************
@app.route('/home/timeline/delete_post/<post_to_delete_id>')
@login_required
def delete_post(post_to_delete_id):
    post_id = int(post_to_delete_id)
    post = Post.query.filter_by(post_id = int(post_to_delete_id))

    if post.username == current_user.username: # Owned post
        db.session.delete(post)
        db.session.commit()
    else: # Repost
        repost = Repost.query.filter_by(post_id = post_id, 
          username = current_user.username).first()
        db.session.delete(repost)
        db.session.commit()

    return redirect(url_for('user_timeline'))

#*******************
#***Edit*post***
#*******************
@app.route('/home/timeline/edit_post/prompt/<post_to_edit_id>', methods=['GET', 'POST'])
@login_required
def edit_post_prompt(post_to_edit_id):
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()

    # Retrieves the content of the original message to populate the edit prompt screen to aid in modifying a post
    original_post_content = ""
    original_post_attachment= ""
    post_database_table = Post.query.all()
    for post in post_database_table:
        if (post.post_id == int(post_to_edit_id)):
            original_post_content = post.post_text
            original_post_attachment = post.post_media

    return render_template('edit_timeline_post.html', post_to_edit_id=post_to_edit_id, user = queried_user, original_post_content=original_post_content, original_post_attachment=original_post_attachment)

#*************************
#***Edit*post*(cont.)***
#*************************
@app.route('/home/timeline/edit_post/<post_to_edit_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_to_edit_id):
    post_database_table = Post.query.all()
    for post in post_database_table:
        if (post.post_id == int(post_to_edit_id)):
            post.post_text = request.form.get('edit_text')
            post.last_edit_time = datetime.now()
    
            # Reads in the media attached to a post
            # Source: https://www.youtube.com/watch?v=6WruncSoCdI
            if request.method == "POST":
                if request.files:

                    media = request.files['edit_media']

                    if not media.filename == "":
                        if allowed_media(media.filename):
                            filename = secure_filename(media.filename)
                            media.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                            post.post_media = filename
                            
                        else:
                            flash('That file extension is not allowed.')
                    else:
                        None
    
    db.session.commit()

    return redirect(url_for('user_timeline'))

#***********************
#***Logout*of*Account***
#***********************
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#*************************
#***User's*account*page***
#*************************
@app.route('/home/account')
@login_required
def user_account():
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()

    return render_template('account.html')

#***********************
#***User's*about*page***
#***********************
@app.route('/home/account/about')
@login_required
def about():
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()

    return render_template('about.html', user = queried_user)

#*****************************
#***User's*account*settings***
#*****************************
@app.route('/home/account/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()
    
    return render_template('settings.html', user = queried_user)

#******************************
#***Account*Settings*Editing***
#******************************
@app.route('/home/account/settings/editing', methods=['GET', 'POST'])
@login_required
def edit_account():
    # Retrieves the information associated with the current user to display on the account page
    queried_user = User.query.filter_by(username = current_user.username).first()

    if request.method == "POST":
        if request.files:

            media_1 = request.files['profile_picture']
            media_2 = request.files['background_banner_image']

            if not media_1.filename == "":
                if allowed_image_media(media_1.filename):
                    filename = secure_filename(media_1.filename)
                    media_1.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                    queried_user.profile_picture = filename
                    
                else:
                    flash('That file extension is not allowed.')
                    return redirect(url_for('user_settings'))
            else:
                None

            if not media_2.filename == "":
                if allowed_image_media(media_2.filename):
                    filename = secure_filename(media_2.filename)
                    media_2.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                    queried_user.background_banner_image = filename
                    
                else:
                    flash('That file extension is not allowed.')
                    return redirect(url_for('user_settings'))
            else:
                None

    queried_user.user_description = request.form.get('user_description')
    queried_user.objective = request.form.get('objective')
    queried_user.phone_number = request.form.get('phone_number')

    db.session.commit()

    return redirect(url_for('user_settings'))

#*************************
#***User's*friends*page***
#*************************
@app.route('/home/account/friends')
@login_required
def user_friends():
    friends, sent_requests, received_requests = [], [], []

    # Friends
    friends_1 = Relationship.query.filter_by(
      username_1 = current_user.username, 
      relationship_type = RelationshipType.FRIEND
    ).all()
    friends_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.FRIEND
    ).all()
    for friend in friends_1:
        friends.append(friend.username_2)
    for friend in friends_2:
        friends.append(friend.username_1)

    # Users you have sent a friend request
    sent_requests_1 = Relationship.query.filter_by(
      username_1 = current_user.username,
      relationship_type = RelationshipType.SENT_REQUEST
    ).all()
    sent_requests_2 = Relationship.query.filter_by(
      username_2 = current_user.username, 
      relationship_type = RelationshipType.RECEIVED_REQUEST
    ).all()
    for receiver in sent_requests_1:
        sent_requests.append(receiver.username_2)
    for receiver in sent_requests_2:
        sent_requests.append(receiver.username_1)

    # Users you have received a friend request from
    received_requests_1 = Relationship.query.filter_by(
      username_1 = current_user.username,
      relationship_type = RelationshipType.RECEIVED_REQUEST
    ).all()
    received_requests_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.SENT_REQUEST
    ).all()
    for sender in received_requests_1:
        received_requests.append(sender.username_2)
    for sender in received_requests_2:
        received_requests.append(sender.username_1)


    return render_template('friends.html', friends=friends, 
      received_requests=received_requests, sent_requests=sent_requests)

#***************************************
#***Change relationship between users***
#***************************************
@app.route('/modify_relationship/<username>?redirect=<redirect_page>')
@login_required
def modify_relationship(username, redirect_page):
    # current_user (new_relationship) foreign_user
    foreign_user = User.query.filter_by(username = username).first()
    new_relationship = request.form.get('new_relationship')

    # Page was accessed by typing in the url
    if new_relationship == None:
        flash('You do not have permission to use that url')
        return redirect(url_for('user_timeline'))

    # Change database to reflect new relationship between users

#************
#***Search***
#************
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    username = request.form.get('search_bar_input')
    foreign_user = User.query.filter_by(username = username).first()

    if foreign_user == None:
        flash('There is no account with that username.')
        return redirect(url_for('user_timeline'))

    if foreign_user.username == current_user.username:
        return redirect(url_for('user_timeline'))

    return redirect(url_for('foreign_timeline', username=username))

#***********************
#***Foreign*Timeline****
#***********************
@app.route('/user/<username>')
@login_required
def foreign_timeline(username):
    foreign_user = User.query.filter_by(username = username).first()

    # Determine order in database
    username_1, username_2 = current_user.username, foreign_user.username
    if current_user.username > foreign_user.username:
        username_1 = foreign_user.username
        username_2 = current_user.username
    relationship = Relationship.query.filter_by(username_1 = username_1,
      username_2 = username_2).first()

    # Not friends
    if relationship == None:
        return render_template('foreign_timeline_locked.html', username=username)
    if relationship.relationship_type != RelationshipType.FRIEND:
        return render_template('foreign_timeline_locked.html', username=username)

    foreign_timeline = Post.query.filter_by(username = foreign_user.username)
    foreign_timeline = foreign_timeline.order_by(Post.original_post_time.desc())
    foreign_timeline = foreign_timeline.all()

    # TODO: Order with reposts

    return render_template('foreign_timeline.html', username=username, 
      timeline = foreign_timeline)

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
