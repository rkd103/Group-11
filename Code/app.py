# Library Includes
from class_objects import User 
from flask import Flask, render_template, redirect, request
# Creates an instance of a Flask object
app = Flask(__name__)


# Adds a function that returns content using Flask's decorator to map the URL route (/) to that function
@app.route("/")
# Function Declaration and Defintion
def home():
    return render_template("home.html")

@app.route("/login", methods=['GET', 'POST'])
# Function Declaration and Defintion
def login():
    current_user = User(request.form['username'], request.form['password'])
    return render_template('login.html', username=current_user.username, password=current_user.password)

@app.route("/forget_password")
# Function Declaration and Defintion
def forgot_password():
    return "<h1>Forgot password? button pressed!</h1>"

@app.route("/create_account")
# Function Declaration and Defintion
def create_account():
    return "<h1>Create new account button pressed!</h1>"

# Driver code
# Specifies the localhost
if __name__ == "__main__":
    app.run(host='0.0.0.0')