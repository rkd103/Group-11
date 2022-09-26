# Library Includes
from class_objects import User 
from flask import Flask, render_template, redirect, request
# Creates an instance of a Flask object
app = Flask(__name__)


# Adds a function that returns content using Flask's decorator to map the URL route (/) to that function
@app.route("/")
# Function Declaration and Defintion
def home():
    account_creation_flag = 0;
    return render_template("home.html", account_creation_flag=account_creation_flag)

@app.route("/login", methods=['GET', 'POST'])
# Function Declaration and Defintion
def login():
    current_user = User(username=request.form['username'], password=request.form['password'])
    # Change to redirect to the user's account page
    # Validate with database
    return render_template('login.html', username=current_user.username, password=current_user.password)

@app.route("/forgot_credentials")
# Function Declaration and Defintion
def forgot_credentials():
    return render_template('forgot_credentials.html')

@app.route("/account_retrival", methods=['GET', 'POST'])
# Function Declaration and Defintion
def account_retrival():
    current_user = User(username=request.form['username'], password=request.form['password'])
    # search database based on whichever field is not empty
    return render_template('account_retrival.html', username=current_user.username, password=current_user.password)

@app.route("/create_account")
# Function Declaration and Defintion
def create_account():
    password_input_flag = 0;
    return render_template('create_account.html', password_input_flag=password_input_flag)

@app.route("/validate_credentials", methods=['GET', 'POST'])
# Function Declaration and Defintion
def validate_credentials():
    current_user = User(username=request.form['username'], password=request.form['password'], first_name=request.form['first_name'], middle_name=request.form['middle_name'], last_name=request.form['last_name'], email=request.form['email'], password_confirmation=request.form['password_confirmation'])
    account_creation_flag = 1;
    password_input_flag = 0;
    if(current_user.password != current_user.password_confirmation):
        password_input_flag = 1;
        return render_template("create_account.html", password_input_flag=password_input_flag)
    else:
        # Send data to database
        return render_template('home.html', account_creation_flag=account_creation_flag)

# Driver code
# Specifies the localhost
if __name__ == "__main__":
    app.run(host='0.0.0.0')