from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash    #securing passwords 
from .. import db
from flask_login import login_required, login_user, logout_user, current_user
from ..forms import ContactForm



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #search db by a specific field. Login process to check what user entered with whats in the db
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                profile = user.profile
                if profile == "seeker":
                    if request.form.get('profile') == "seeker":
                        flash('Logged in successfully.', category='success')
                        login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
                        return redirect(url_for('main.seeker_home')) #redirect to the page 
                    else:
                        flash('Did not log in successfully because the user is of wrong type. Probably employer', category='error')
                if profile == "employer":
                    if request.form.get('profile') == "employer":
                        flash('Logged in successfully.', category='success')
                        login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
                        return redirect(url_for('main.employer_home'))
                    else:
                        flash('Did not log in successfully because the user is of wrong type. Probably seeker', category='error')
                if profile == "admin":
                    if request.form.get('profile') == "admin":
                        flash('Logged in successfully.', category='success')
                        login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
                        return redirect(url_for('main.admin_home'))
                    else:
                        flash('Did not log in successfully because the user is of wrong type. This is for admins', category='error')
            else: 
                flash('Incorrect password.', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("auth/login.html", user=current_user)

@auth.route('/logout')
@login_required #can only access the logout function if a user is logged in. 
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    return redirect(url_for('views.seeker_home'))

@auth.route('/user-type', methods=['GET', 'POST'])
def user_type():
    return render_template('auth/selection_type.html', user = current_user)

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
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error') #flashes error message
        elif len(first_name) < 2:
            flash('First name must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 1:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            user = User(profile="seeker",email=email, first_name=first_name, last_name=last_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.seeker_home'))
    return render_template("auth/signup.html", user=current_user)

@auth.route('/signup_employer', methods=['GET', 'POST'])
def signup_employer():
    if request.method == 'POST': 
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #checks if the email is already in use 
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error') #flashes error message
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 1:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            user = User(profile="employer",email=email, company_name=company_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.employer_home'))
    return render_template("auth/signup_employer.html", user=current_user)

@auth.route('/signup_admin', methods=['GET', 'POST'])
def signup_admin():
    if request.method == 'POST': 
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        secret = request.form.get('secret')

        #checks if the email is already in use 
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 2:
            flash('Email must be greater than 4 characters.', category='error') #flashes error message
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 1:
            flash('Password must be greater than 6 characters.', category='error')
        elif secret == 'temporary':
            user = User(profile="admin",email=email, company_name=company_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.admin_home'))
        else:
            flash('The secret key is incorrect', category='error')
    return render_template("auth/signup_admin.html", user=current_user)