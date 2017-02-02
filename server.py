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

@app.route('/register')
def user_registration():
    """User registration page"""

    return render_template("user_registration.html")

@app.route('/process_registration', methods=['POST'])
def process_registration():
    """ Authenticating user.
    TODO: change /process_login to /register, because this route is about
    registering new users.  Also need to create separate route for signing in,
    for existing users."
    """

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        User.query.filter(User.email == email).one()
        flash("This user is already registered.  Please login.")
        return redirect('/login')
    except sqlalchemy.orm.exc.NoResultFound:
        print "User does not exist yet - creating new user"
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("This user successfully registered.")

    print email, password
    return redirect("/")

@app.route('/login')
def login():
    """ Logging user. """

    return render_template('login.html')

@app.route('/process_login', methods=['POST'])
def process_login():

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = User.query.filter(User.email == email).one()
        if user.password == password:
            session['user_id'] = user.user_id
            print session

            flash("This user successfully Login.")
            return redirect("/")
        else:
            flash("Sorry, password did not match. Please try again")
            return redirect("/login")

    except sqlalchemy.orm.exc.NoResultFound:
        flash("User does not exist yet.  Please register a new user")
        return redirect("/register")


@app.route('/logout')
def logout():
    del session['user_id']
    flash("You have successfully logged out.")
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
