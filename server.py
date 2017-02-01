"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

import sqlalchemy


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users = users)

@app.route('/login')
def user_login():
    """User sign-in page"""

    return render_template("user_login.html")

@app.route('/process_login', methods = ['POST'])
def process_login():
    """ Authenticating user.
    TODO: change /process_login to /register, because this route is about
    registering new users.  Also need to create separate route for signing in,
    for existing users."
    """

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        User.query.filter(User.email == email).one()
        print "User exists"
    except sqlalchemy.orm.exc.NoResultFound:
        print "User does not exist yet - creating new user"
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    print email, password
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=8000, host='0.0.0.0')
