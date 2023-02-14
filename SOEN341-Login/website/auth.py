from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User_seeker
from werkzeug.security import generate_password_hash, check_password_hash    #securing passwords 
from . import db
from flask_login import login_required, login_user, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #search db by a specific field. Login process to check what user entered with whats in the db
        user = User_seeker.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
                return redirect(url_for('views.seeker_home')) #redirect to the page 
            else: 
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #can only access the logout function if a user is logged in. 
def logout():
    logout_user()
    #return render_template("auth.login")
    return render_template("login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST': 
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #checks if the email is already in use 
        user = User_seeker.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error') #flashes error message
        elif len(first_name) < 2:
            flash('First name must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            user = User_seeker(email=email, first_name=first_name, last_name=last_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)