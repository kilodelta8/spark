#------------------------------------------------------------------------------------------------
#         Name: Craxer Spark!
#      Version: 0.0.1
#         Date: 2021-09-30
#       Author: John Durham
#      License: MIT*
#  Description: Company wide ERP system, from customer to delivery and everything in between.
#------------------------------------------------------------------------------------------------

#################################################################################################
#   Setup & Imports                                                                             #
#################################################################################################
import sys
from flask import Flask, render_template, url_for, flash, session, request, redirect
from wtforms import Form, StringField, IntegerField, PasswordField, TextAreaField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from datetime import datetime

#application init and configurations
app = Flask(__name__)
app.secret_key = 'lamepass1234' #sys.argv[1]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://sparks:Sparks1234@localhost:8889/sparks"  
app.config['SQLALCHEMY_ECHO'] = True

#initialize instance of db
db = SQLAlchemy(app)






#################################################################################################
#   Models                                                                                      #
#################################################################################################

#user model
class User(db.Model): 
    employeeID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    #init a user
    def __init__(self, employeeID, username, firstName, lastName, email, password):
        self.employeeID = employeeID
        self.username = username
        self.firstName = firstName  
        self.lastName = lastName
        self.email = email
        self.password = password
    #reppin again....
    def __repr__(self):
        return self.employeeID







#################################################################################################
#   Forms                                                                                       #
#################################################################################################

#Registration form
class RegistrationForm(Form): 
    employeeID = IntegerField('Employee ID', [validators.NumberRange(min=1, max=100000000001), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=6, max=30), validators.DataRequired()])
    firstName = StringField('First Name', [validators.Length(min=2, max=30), validators.DataRequired()])
    lastName = StringField('Last Name', [validators.Length(min=2, max=30), validators.DataRequired()])
    email = StringField('Email', [validators.Length(max=120), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=7), validators.DataRequired()])
    verify = PasswordField('Verify Password', [validators.DataRequired()])
    submit = SubmitField('Submit')


#Login form
class LoginForm(Form): 
    username = StringField('Username', [validators.Length(min=6, max=30), validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=7), validators.DataRequired()])
    submit = SubmitField('Submit')








#################################################################################################
#   Routes                                                                                      #
#################################################################################################

#home - landing page route
@app.route('/home')
def home():
    return render_template('home.html', title='Home')



#login to account
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        hashed = existing_user.password
        if pbkdf2_sha256.verify(password, hashed):
            session['username'] = existing_user.username
            session['logged_in'] = True
            flash('You are now logged in!', 'success')
            return redirect('/')
        elif not existing_user:
            flash('Error with your username!', 'danger')
            return redirect(url_for('login'))
        else:
            flash('Password is incorrect', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Login', form=form)
    

#signup for an account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        employeeID = request.form['employeeID']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(employeeID=employeeID).first()
        existing_email = User.query.filter_by(email=email).first()
        if password != verify:
            flash('Your passwords do not match, try again!', 'danger')
            return redirect(url_for('signup'))
        if not existing_email or not existing_user:
            new_user = User(employeeID, firstName, lastName, username, email, pbkdf2_sha256.hash(password))
            db.session.add(new_user)
            db.session.commit()
            session['username'] = new_user.username
            session['employeeID'] = new_user.employeeID
            session['logged_in'] = True
            return redirect('/')
        elif len(existing_user) > 0:  
            flash('That username is already in use, try again!', 'danger')
            return redirect(url_for('signup'))
        elif len(existing_email) > 0:
            flash('That email is already in use, try again!', 'danger')
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html', title='Signup!', form=form)



@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')






#<<<-------------------------------------------------------->>>
if __name__ == '__main__':
    app.run(debug=True)