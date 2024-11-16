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
from wtforms import Form, StringField, PasswordField, TextAreaField, SubmitField, validators
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from datetime import datetime

#application init and configurations
app = Flask(__name__)
app.secret_key = sys.argv[1]
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://spark:PASSWORD123456@localhost:3306/spark"  
app.config['SQLALCHEMY_ECHO'] = True

#initialize instance of db
db = SQLAlchemy(app)






#################################################################################################
#   Models                                                                                      #
#################################################################################################

#user model
class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))
    #init a user
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    #reppin again....
    def __repr__(self):
        return self.username







#################################################################################################
#   Forms                                                                                       #
#################################################################################################

#Registration form
class RegistrationForm(Form): 
    username = StringField('Username', [validators.Length(min=6, max=30), validators.DataRequired()])
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



@app.before_request
def require_login():
    allowed_routes = ['login']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')






#<<<-------------------------------------------------------->>>
if __name__ == '__main__':
    app.run(debug=True)