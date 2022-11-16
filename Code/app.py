#**********************
#***Library*Includes***
#**********************
from tempfile import tempdir
from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
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
import operator
from flask_session import Session


#******************************************
#***Function*Declarations*and*Defintions***
#******************************************
def generate_password():
    rstr = Rstr(SystemRandom())
    return (rstr.xeger(r'[a-zA-z0-9]{7}[0-9]{1}[^a-zA-z0-9\n\t\r\s]{7}'))

# Source: https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/
def send_email(recipient_email, email_subject_line, email_content):
    message = Message   (
                            email_subject_line,
                            sender='cse.4212.group.11@gmail.com',
                            recipients=[recipient_email]
                        )
    message.body = email_content

    mail.send(message)


#********************************************
#***Object*Instantiation*and*Configuration***
#********************************************

# Declares the web application's extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
server_session = Session()

# Further configures the login manager
login_manager.login_view = 'login'
@login_manager.user_loader
def user_loader(username):
    return User.query.get(username)

# Application Factory: Packages the process of setting up a web application in a function.
def create_app():
    # Creates an instance of a Flask object
    app = Flask(__name__)

    # Configures the session variable
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SERVER_TYPE'] = 'sqlalchemy'
    app.config.update(                                                     
    SESSION_COOKIE_DOMAIN = None                                                
)

    # Configures the SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config['SECRET_KEY'] = 'T@&5RcGyBwXbVjb^%VX3'

    # Configures storage mechanism and file/text handlers
    UPLOADS = os.path.join('static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOADS
    app.config['ALLOWED_MEDIA_EXTENSIONS'] = ["PNG", "JPEG", "JPG", "GIF", "MP4", "MOV", "MKV"]
    app.config['MAX_CONTENT_LENGTH'] = (10 * 1024 * 1024)
    app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG", "JPEG", "JPG", "GIF"]

    # Configures mail subsystem
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'cse.4212.group.11@gmail.com'
    app.config['MAIL_PASSWORD'] = base64.b64decode('amVvemZwaGxjdWthd3dtZQ==').decode("utf-8")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    # Initializes the subsystems
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    server_session.init_app(app)

    return app

# Using the application factory, sets up an instance of the website
app = create_app()

# Source: https://www.youtube.com/watch?v=6WruncSoCdI
def allowed_media(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_MEDIA_EXTENSIONS']:
        return True
    else:
        return False

def allowed_image_media(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False

# Source: https://stackoverflow.com/questions/19459236/how-to-handle-413-request-entity-too-large-in-python-flask-server
@app.errorhandler(413)
def request_entity_too_large(error):
    flash('That file is too large.\n\nIt exceeded the maximum size of 10MB.')
    return redirect(url_for('user_account'))

# Customizes the "not found" error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html')

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

# username_1 and username_2 based on alphabetical order
# username_1 (relationship) username_2
# No row in table -> no relationship
class RelationshipType(enum.Enum):
    NO_RELATIONSHIP = 0 # Used only for backend purposes, not stored in db
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
    original_post_time = db.Column(db.TIMESTAMP, nullable=False)
    last_edit_time = db.Column(db.TIMESTAMP, nullable=True)
    post_media = db.Column(db.String(1024), nullable=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1024), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.String(1024), nullable=False)
    original_comment_time = db.Column(db.TIMESTAMP, nullable=False)
    last_edit_time = db.Column(db.TIMESTAMP, nullable=True)

class Share(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)
    shared_time = db.Column(db.TIMESTAMP, nullable=False)

class PostLikes(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

class CommentLikes(db.Model):
    comment_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(1024), nullable=False, primary_key=True)

class FriendMessage(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(1024), nullable=False)
    receiver = db.Column(db.String(1024), nullable=False)
    message_text = db.Column(db.String(1024), nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)

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

#**********************************
#***Helper*functions*And*Classes***
#**********************************

def verify_friendship(username_1, username_2):
    if username_1 > username_2:
        temp = username_2
        username_2 = username_1
        username_1 = temp
    
    relationship = Relationship.query.filter_by(username_1 = username_1,
      username_2 = username_2).first()

    if relationship == None:
        return False
    if relationship.relationship_type != RelationshipType.FRIEND:
        return False
    return True

# Class which includes derived attributes for Comment
class TimelineComment():
    def __init__(self, comment):
        self.comment = comment
        self.num_likes = self.get_num_likes()
    
    def get_num_likes(self):
        likes = CommentLikes.query.filter_by(
          comment_id = self.comment.comment_id
        ).all()
        return len(likes)

# Class for displaying timeline posts
class TimelinePost():
    def __init__(self, post, is_share):
        self.post = post
        self.is_share = is_share
        self.comments = self.get_post_comments()
        self.num_visible_comments = len(self.comments)
        self.time = self.get_post_time()
        self.num_likes = self.get_num_likes()
        self.num_shares = self.get_num_shares()
        self.num_comments = self.get_num_comments()
    
    # Get timeline posts visible to the user (comments made by mutual friends)
    def get_post_comments(self):
        comments = Comment.query.filter_by(
          parent_id = self.post.post_id
        ).all()

        friends = []
        friends_1 = Relationship.query.filter_by(
            username_1 = current_user.username, 
            relationship_type = RelationshipType.FRIEND
        ).all()
        friends_2 = Relationship.query.filter_by(
            username_2 = current_user.username,
            relationship_type = RelationshipType.FRIEND
        ).all()
        for relationship in friends_1:
            friends.append(relationship.username_2)
        for relationship in friends_2:
            friends.append(relationship.username_1)
        comments = [comment for comment in comments 
                    if comment.username in friends 
                    or comment.username == current_user.username]

        comments = sorted(
          comments, key = operator.attrgetter('original_comment_time')
        )

        # Convert to class which has derived attributes for comment
        timeline_comments = []
        for comment in comments:
            timeline_comments.append(TimelineComment(comment))
        
        return timeline_comments

    def get_post_time(self):
        if self.is_share:
            share = Share.query.filter_by(
              post_id = self.post.post_id
            ).first()
            return share.shared_time
        else:
            return self.post.original_post_time

    def get_num_likes(self):
        likes = PostLikes.query.filter_by(post_id = self.post.post_id).all()
        return len(likes)
    def get_num_shares(self):
        shares = Share.query.filter_by(post_id = self.post.post_id).all()
        return len(shares)
    def get_num_comments(self):
        comments = Comment.query.filter_by(parent_id = self.post.post_id).all()
        return len(comments)

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
    session['url'] = url_for('user_timeline')
    timeline = []

    # Get all user posts
    user_posts = Post.query.filter_by(username = current_user.username).all()
    for post in user_posts:
        timeline.append(TimelinePost(post, False))
    
    # Get all user shares
    shares = Share.query.filter_by(username = current_user.username).all()
    for share in shares:
        post = Post.query.filter_by(post_id = share.post_id).first()
        timeline.append(TimelinePost(post, True))

    # Order posts and shares based on time shared/posted
    timeline = sorted(timeline, key = operator.attrgetter('time'), reverse = True)

    return render_template('personal_timeline.html', timeline = timeline, user = current_user)

#***********************
#***Submit*a*new*post***
#***********************
@app.route('/home/timeline/submit_post', methods=['GET', 'POST'])
@login_required
def submit_post():
    if request.method != 'POST':
        return redirect(url_for('user_timeline')) 

    # Generate unique post id
    new_post_id = randrange(pow(2, 31) - 1)
    while Post.query.filter_by(post_id = new_post_id).first() != None:
        new_post_id = randrange(pow(2, 31) - 1)

    # Add new post to database
    new_post = Post(
      post_id = new_post_id, username = current_user.username,
      post_text = request.form.get('post_text'),
      original_post_time = datetime.now(),
      last_edit_time = None, post_media = ""
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

#****************************
#***Delete*a*post*or*share***
#****************************
@app.route('/home/timeline/delete_post/<post_to_delete_id>')
@login_required
def delete_post(post_to_delete_id):
    post_to_delete_id = int(post_to_delete_id)
    post = Post.query.filter_by(post_id = post_to_delete_id).first()

    if post == None:
        flash('That post no longer exists.')
        return redirect(url_for('user_timeline'))

    if post.username == current_user.username: # User post
        # Cascade deletion through db
        likes = PostLikes.query.filter_by(post_id = post_to_delete_id).all()
        shares = Share.query.filter_by(post_id = post_to_delete_id).all()
        comments = Comment.query.filter_by(parent_id = post_to_delete_id).all()
        for like in likes:
            db.session.delete(like)
        for share in shares:
            db.session.delete(share)
        for comment in comments:
            db.session.delete(comment)

        db.session.delete(post)
        db.session.commit()
    else: # Share
        share = Share.query.filter_by(
          post_id = post_to_delete_id, username = current_user.username
        ).first()

        if share == None: # User does not own and hasn't shared the post
            return redirect(url_for('user_timeline'))

        db.session.delete(share)
        db.session.commit()
    
    return redirect(url_for('user_timeline'))
        
#***************
#***Edit*post***
#***************
@app.route('/home/timeline/edit_post/prompt/<post_to_edit_id>', methods=['GET', 'POST'])
@login_required
def edit_post_prompt(post_to_edit_id):
    # Retrieves the content of the original message to populate the edit prompt
    # screen to aid in modifying a post
    original_post_content = ""
    original_post_attachment= ""

    post = Post.query.filter_by(post_id = int(post_to_edit_id)).first()

    if post == None:
        return redirect(session['url'])
    if post.username != current_user.username:
        return redirect(session['url'])
    
    original_post_content = post.post_text
    original_post_attachment = post.post_media

    return render_template(
      'edit_timeline_post.html', post_to_edit_id=post_to_edit_id, 
      user = current_user, original_post_content=original_post_content, 
      original_post_attachment=original_post_attachment
    )

#***********************
#***Edit*post*(cont.)***
#***********************
@app.route('/home/timeline/edit_post/<post_to_edit_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_to_edit_id):
    session['url'] = url_for('user_timeline')

    post = Post.query.filter_by(post_id = int(post_to_edit_id)).first()

    if post == None:
        return redirect(session['url'])
    if post.username != current_user.username:
        return redirect(session['url'])
    
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
    
    db.session.commit()
    return redirect(session['url'])

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
@app.route('/home')
@app.route('/home/')
@app.route('/home/account')
@login_required
def user_account():
    return render_template('account.html', user = current_user)

#***********************
#***User's*about*page***
#***********************
@app.route('/home/account/about')
@login_required
def about():
    return render_template('about.html', user = current_user)

@app.route('/home/account/friends')
@login_required
def user_friends():
    session['url'] = url_for('user_friends')
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
    for relationship in friends_1:
        friends.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in friends_2:
        friends.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    # Users you have sent a friend request
    sent_requests_1 = Relationship.query.filter_by(
      username_1 = current_user.username,
      relationship_type = RelationshipType.SENT_REQUEST
    ).all()
    sent_requests_2 = Relationship.query.filter_by(
      username_2 = current_user.username, 
      relationship_type = RelationshipType.RECEIVED_REQUEST
    ).all()
    for relationship in sent_requests_1:
        sent_requests.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in sent_requests_2:
        sent_requests.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    # Users you have received a friend request from
    received_requests_1 = Relationship.query.filter_by(
      username_1 = current_user.username,
      relationship_type = RelationshipType.RECEIVED_REQUEST
    ).all()
    received_requests_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.SENT_REQUEST
    ).all()
    for relationship in received_requests_1:
        received_requests.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in received_requests_2:
        received_requests.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    return render_template(
      'user_friends.html', user = current_user, friends = friends, 
      sent_requests = sent_requests, received_requests = received_requests
    )

#*****************************
#***User's*account*settings***
#*****************************
@app.route('/home/account/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    return render_template('settings.html', user = current_user)

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

    queried_user.user_description = request.form.get('user_description')
    queried_user.objective = request.form.get('objective')
    queried_user.phone_number = request.form.get('phone_number')

    db.session.commit()

    return redirect(url_for('user_settings'))

#**********************
#***Search*for*Users***
#**********************
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    username = request.form.get('search_bar_input')
    foreign_user = User.query.filter_by(username = username).first()

    if foreign_user == None:
        flash("The queried user does not exist.")
        return redirect(url_for('user_account'))
    if current_user.username == foreign_user.username:
        flash("You are currently logged in. Search for another user.")
        return redirect(url_for('user_account'))

    return redirect(url_for('foreign_account', username = username))

#**************************
#***Foreign*User*Account***
#**************************
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def foreign_account(username):
    session['url'] = url_for('foreign_account', username = username)
    foreign_user = User.query.filter_by(username = username).first()

    if current_user.username == foreign_user.username:
        return redirect(url_for('user_timeline'))

    # Determine order in database
    username_1, username_2 = current_user.username, foreign_user.username
    if current_user.username > foreign_user.username:
        username_1 = foreign_user.username
        username_2 = current_user.username

    relationship = Relationship.query.filter_by(
      username_1 = username_1, username_2 = username_2
    ).first()

    # Not friends
    pending_request = False
    if relationship == None:
        return render_template(
          'foreign_account_locked.html', user = current_user, 
          foreign_user = foreign_user, pending_request = pending_request
        )
    if relationship.relationship_type != RelationshipType.FRIEND:
        if username_1 == current_user.username:
            if relationship.relationship_type == RelationshipType.SENT_REQUEST:
                pending_request = True
        else:
            if relationship.relationship_type == RelationshipType.RECEIVED_REQUEST:
                pending_request = True
        return render_template(
          'foreign_account_locked.html', user = current_user, 
          foreign_user = foreign_user, pending_request = pending_request
        )

    # Friends
    return render_template('foreign_account.html', user = current_user, 
      foreign_user = foreign_user)

#***************************
#***Foreign*User*Timeline***
#***************************
@app.route('/user/<username>/timeline')
@login_required
def foreign_timeline(username):
    session['url'] = url_for('foreign_timeline', username = username)
    foreign_user = User.query.filter_by(username = username).first()
    timeline = []

    if not verify_friendship(current_user.username, foreign_user.username):
        flash('You must be friends to view that page.')
        return redirect(url_for(
          'foreign_account', username = foreign_user.username
        ))
    
    # Get all foreign user posts
    posts = Post.query.filter_by(username = foreign_user.username).all()
    for post in posts:
        timeline.append(TimelinePost(post, False))
    
    # Get friends of user
    friends = []
    friends_1 = Relationship.query.filter_by(
      username_1 = current_user.username, 
      relationship_type = RelationshipType.FRIEND
    ).all()
    friends_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.FRIEND
    ).all()
    for relationship in friends_1:
        friends.append(relationship.username_2)
    for relationship in friends_2:
        friends.append(relationship.username_1)

    # Get shares of mutual friends
    shares = Share.query.filter_by(username = foreign_user.username).all()
    for share in shares:
        original_post = Post.query.filter_by(post_id = share.post_id).first()
        if original_post.username not in friends:
            continue

        post = Post.query.filter_by(post_id = share.post_id).first()
        timeline.append(TimelinePost(post, True))

    # Get foreign user posts already shared by user
    already_shared = []
    shares = Share.query.filter_by(username = current_user.username).all()
    for share in shares:
        post = Post.query.filter_by(post_id = share.post_id).first()

        if post == None:
            continue
        if post.username != foreign_user.username:
            continue

        already_shared.append(post)

    return render_template(
      'foreign_timeline.html', user = current_user, 
      foreign_user = foreign_user, timeline = timeline,
      already_shared = already_shared 
    )

#***************************
#***Foreign*User*About******
#***************************
@app.route('/user/<username>/about')
@login_required
def foreign_about(username):
    foreign_user = User.query.filter_by(username = username).first()

    if not verify_friendship(current_user.username, foreign_user.username):
        flash('You must be friends to view that page.')
        return redirect(url_for(
          'foreign_account', username = foreign_user.username
        ))
    
    return render_template('foreign_about.html', user = current_user, 
      foreign_user = foreign_user)

@app.route('/user/<username>/friends')
@login_required
def foreign_friends(username):
    foreign_user = User.query.filter_by(username = username).first()

    if not verify_friendship(current_user.username, foreign_user.username):
        flash('You must be friends to view that page.')
        return redirect(url_for(
          'foreign_account', username = foreign_user.username
        ))

    # Friends
    friends = []
    friends_1 = Relationship.query.filter_by(
      username_1 = foreign_user.username, 
      relationship_type = RelationshipType.FRIEND
    ).all()
    friends_2 = Relationship.query.filter_by(
      username_2 = foreign_user.username,
      relationship_type = RelationshipType.FRIEND
    ).all()
    for relationship in friends_1:
        friends.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in friends_2:
        friends.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    return render_template('foreign_friends.html', user = current_user, 
      foreign_user = foreign_user, friends = friends)

#****************************************
#***Change*relationships*between*users***
#****************************************
# Change the database to reflect the new relationship between users
# when friend requests are sent/received and accepted/rejected
@app.route('/modify_relationship/<username>', methods=['GET', 'POST'])
@login_required
def modify_relationship(username):
    if request.method != 'POST':
        return redirect(session['url'])

    # current_user (relationship) foreign_user
    new_relationship_type = request.form.get('new_relationship_type')
    foreign_user = User.query.filter_by(username = username).first()
    
    # Determine order of usernames in database
    inverted_relationship = False
    username_1, username_2 = current_user.username, foreign_user.username
    if current_user.username > foreign_user.username:
        username_1 = foreign_user.username
        username_2 = current_user.username
        inverted_relationship = True

    new_relationship_type = RelationshipType[new_relationship_type]
    if inverted_relationship: # foreign_user (relationship) current_user
        if new_relationship_type == RelationshipType.SENT_REQUEST:
            new_relationship_type = RelationshipType.RECEIVED_REQUEST

    current_relationship = Relationship.query.filter_by(
      username_1 = username_1, username_2 = username_2
    ).first()

    # This prevents someone from modifying form data with inspect
    # and adding friends that way.
    if new_relationship_type == RelationshipType.FRIEND:
        return redirect(session['url'])
    
    if current_relationship == None:
        new_relationship = Relationship(
          username_1 = username_1, username_2 = username_2,
          relationship_type = new_relationship_type
        )
        db.session.add(new_relationship)
        db.session.commit()
    elif new_relationship_type == RelationshipType.NO_RELATIONSHIP: 
        # Remove user's likes, shares, and comments on foreign user's posts
        posts = Post.query.filter_by(username = foreign_user.username).all()
        for post in posts:
            PostLikes.query.filter_by(
              post_id = post.post_id, username = current_user.username
            ).delete()
            Share.query.filter_by(
              post_id = post.post_id, username = current_user.username
            ).delete()
            Comment.query.filter_by(
              parent_id = post.post_id, username = current_user.username
            ).delete()
    
        # Remove user's likes on foreign user's comments
        comments = Comment.query.filter_by(username = foreign_user.username).all()
        for comment in comments:
            CommentLikes.query.filter_by(
              comment_id = comment.comment_id, username = current_user.username
            ).delete()

        # Remove foreign user's likes, shares, and comments on user's posts
        posts = Post.query.filter_by(username = current_user.username).all()
        for post in posts:
            PostLikes.query.filter_by(
              post_id = post.post_id, username = foreign_user.username
            ).delete()
            Share.query.filter_by(
              post_id = post.post_id, username = foreign_user.username
            ).delete()
            Comment.query.filter_by(
              parent_id = post.post_id, username = foreign_user.username
            ).delete()

        # Remove foreign user's likes on user's comments
        comments = Comment.query.filter_by(username = current_user.username).all()
        for comment in comments:
            CommentLikes.query.filter_by(
              comment_id = comment.comment_id, username = foreign_user.username
            ).delete()

        # Remove messages between users
        FriendMessage.query.filter_by(
          sender = current_user.username, receiver = foreign_user.username
        ).delete()
        FriendMessage.query.filter_by(
          sender = foreign_user.username, receiver = current_user.username
        ).delete()

        db.session.delete(current_relationship)
        db.session.commit()
    # Mutual friend requests were sent (a user accepting a friend request
    # functions as them sending a friend request to the sender which is
    # automatically accepted)
    else:
        username_1 = current_relationship.username_1
        username_2 = current_relationship.username_2
        relationship_type = RelationshipType.FRIEND

        db.session.delete(current_relationship)
        new_relationship = Relationship(
          username_1 = username_1, username_2 = username_2, 
          relationship_type = relationship_type
        )
        db.session.add(new_relationship)
        db.session.commit()

    return redirect(session['url'])

#********************
#***Submit*comment***
#********************
@app.route('/submit_comment/<post_id>', methods = ['GET', 'POST'])
@login_required
def submit_comment(post_id):
    post_id = int(post_id)
    post = Post.query.filter_by(post_id = post_id).first()

    if post == None:
        flash('That post no longer exists.')
        return redirect(session['url'])
    if request.method != 'POST':
        return redirect(session['url'])
    if not verify_friendship(post.username, current_user.username):
        if post.username != current_user.username:
            return redirect(session['url'])

    # Generate a unique comment id
    new_comment_id = randrange(pow(2, 31) - 1)
    while Comment.query.filter_by(comment_id = new_comment_id).first() != None:
        new_comment_id = randrange(pow(2, 31) - 1)
    
    # Add new comment to database
    new_comment = Comment(
      comment_id = new_comment_id, username = current_user.username,
      parent_id = post.post_id,
      comment_text = request.form.get('comment_text'),
      original_comment_time = datetime.now()
    )
    db.session.add(new_comment)
    db.session.commit()

    return redirect(session['url'])

#********************
#***Delete*comment***
#********************
@app.route('/delete_comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment_id = int(comment_id)
    comment = Comment.query.filter_by(comment_id = comment_id).first()
    
    if comment == None:
        return redirect(session['url'])
    if comment.username != current_user.username:
        return redirect(session['url'])
    
    CommentLikes.query.filter_by(comment_id = comment_id).delete()
    db.session.delete(comment)
    db.session.commit()
    
    return redirect(session['url'])

#******************
#***Edit*comment***
#******************
@app.route('/edit_comment/<comment_id>', methods = ['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment_id = int(comment_id)
    comment = Comment.query.filter_by(comment_id = comment_id).first()
    new_comment_text = request.form.get('edited_comment_text_box')

    if request.method != 'POST':
        return redirect(url_for('user_timeline'))
    if comment == None:
        return redirect(url_for('user_timeline'))
    if comment.username != current_user.username:
        return redirect(url_for('user_timeline'))
    if new_comment_text == comment.comment_text:
        return redirect(url_for('user_timeline'))
    
    comment.comment_text = new_comment_text
    db.session.commit()
    return redirect(session['url'])

@app.route('/share_post/<post_id>')
@login_required
def share_post(post_id):
    post_id = int(post_id)
    post = Post.query.filter_by(post_id = post_id).first()

    if post == None:
        flash('That post no longer exists.')
        return redirect(url_for('user_timeline'))
    if post.username == current_user.username:
        return redirect(url_for('user_timeline'))
    
    share = Post.query.filter_by(
      post_id = post.post_id, username = current_user.username
    ).first()
    if share != None:
        flash('You have already shared this post.')
        return redirect(url_for('user_timeline'))
    
    new_share = Share(
      post_id = post.post_id, username = current_user.username, 
      shared_time = datetime.now()
    )
    db.session.add(new_share)
    db.session.commit()

    return redirect(session['url'])

#**************************
#***Like*and*unlike*post***
#**************************
@app.route('/modify_post_likes/<post_id>')
@login_required
def modify_post_likes(post_id):
    post_id = int(post_id)
    post = Post.query.filter_by(post_id = post_id).first()
    if post == None:
        flash('That post no longer exists.')
        return redirect(session['url'])
    if post.username != current_user.username:
        if not verify_friendship(current_user.username, post.username):
            return redirect(url_for('user_timeline'))
    
    like = PostLikes.query.filter_by(
      post_id = post_id, username = current_user.username
    ).first()

    if like == None:
        new_like = PostLikes(
          post_id = post_id, username = current_user.username
        )
        db.session.add(new_like)
        db.session.commit()
    else:
        db.session.delete(like)
        db.session.commit()
    
    return redirect(session['url'])

#*****************************
#***Like*and*unlike*comment***
#*****************************
@app.route('/modify_comment_likes/<comment_id>')
@login_required
def modify_comment_likes(comment_id):
    comment_id = int(comment_id)
    comment = Comment.query.filter_by(comment_id = comment_id).first()

    if comment == None:
        flash('That comment no longer exists.')
        return redirect(session['url'])
    if current_user.username != comment.username:
        if not verify_friendship(current_user.username, comment.username):
            return redirect(session['url'])
    
    like = CommentLikes.query.filter_by(
      comment_id = comment_id, username = current_user.username
    ).first()

    if like == None:
        new_like = CommentLikes(
          comment_id = comment_id, username = current_user.username
        )
        db.session.add(new_like)
        db.session.commit()
    else:
        db.session.delete(like)
        db.session.commit()
    
    return redirect(session['url'])

@app.route('/messages')
@login_required
def messages():
    session['url'] = url_for('messages')

    friends = []
    friends_1 = Relationship.query.filter_by(
      username_1 = current_user.username, 
      relationship_type = RelationshipType.FRIEND
    ).all()
    friends_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.FRIEND
    ).all()
    for relationship in friends_1:
        friends.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in friends_2:
        friends.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    print(friends)

    return render_template(
      'messages.html', user = current_user, friends = friends
    )

@app.route('/messages/<username>')
@login_required
def chat_log(username):
    session['url'] = url_for('chat_log', username = username)
    foreign_user = User.query.filter_by(username = username).first()

    if foreign_user == None:
        return redirect('messages')
    if not verify_friendship(current_user.username, foreign_user.username):
        return redirect('messages')

    # User friends
    friends = []
    friends_1 = Relationship.query.filter_by(
      username_1 = current_user.username, 
      relationship_type = RelationshipType.FRIEND
    ).all()
    friends_2 = Relationship.query.filter_by(
      username_2 = current_user.username,
      relationship_type = RelationshipType.FRIEND
    ).all()
    for relationship in friends_1:
        friends.append(
          User.query.filter_by(username = relationship.username_2).first()
        )
    for relationship in friends_2:
        friends.append(
          User.query.filter_by(username = relationship.username_1).first()
        )

    # Get chat log
    messages_1 = FriendMessage.query.filter_by(
      sender = current_user.username, receiver = foreign_user.username
    ).all()
    messages_2 = FriendMessage.query.filter_by(
      receiver = current_user.username, sender = foreign_user.username
    ).all()
    messages = messages_1 + messages_2
    messages = sorted(
      messages, key = operator.attrgetter('time')
    )

    return render_template(
      'chat_log.html', user = current_user, foreign_user = foreign_user,
      friends = friends, messages = messages
    )

#*********************
#***Message*Friends***
#*********************
@app.route('/send_message/<username>', methods = ['GET', 'POST'])
@login_required
def send_message(username):
    foreign_user = User.query.filter_by(username = username).first()

    if request.method != 'POST':
        return redirect(session['url'])
    if foreign_user == None:
        return redirect(session['url'])
    if not verify_friendship(current_user.username, foreign_user.username):
        return redirect(session['url'])

    # Generate unique message id
    new_message_id = randrange(pow(2, 31) - 1)
    while FriendMessage.query.filter_by(message_id = new_message_id).first() != None:
        new_message_id = randrange(pow(2, 31) - 1)

    new_message = FriendMessage(
      message_id = new_message_id,
      sender = current_user.username, 
      receiver = foreign_user.username,
      message_text = request.form.get('message_text_box'), 
      time = datetime.now()
    )
    db.session.add(new_message)
    db.session.commit()

    send_notification()
    
    return redirect(session['url'])

def send_notification():
    pass

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
    app.run(host='0.0.0.0', port=5000,)
