from flask import Flask, render_template
from class_objects import User

app = Flask(__name__)

# User for testing purposes
test_user = User('test_username', 'test_password', 'test_first', 'test_middle', 'test_name', 'test_email', 'test_password')

# User's personal timeline
@app.route('/') # TODO: Delete
@app.route('/home')
@app.route('/home/timeline')
def personal_timeline():
    current_user = test_user # TODO: Delete
    return render_template('personal_timeline.html', user = current_user)

# @app.route('/home/timeline/new_post')
# def new_post():
#     current_user = test_user # TODO: Delete
#     return render_template('personal_timeline.html', user = current_user, new_post_flag = True)

# User's friends page
@app.route('/home/friends')
def personal_account():
    current_user = test_user # TODO: Delete
    return render_template('friends.html', user = current_user)

# User's account page
@app.route('/home/account')
def account_management():
    current_user = test_user # TODO: Delete
    return render_template('account.html', user = current_user)

if __name__ == "__main__":
    app.run()