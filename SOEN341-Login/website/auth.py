from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Employer, Admin
from werkzeug.security import generate_password_hash, check_password_hash    #securing passwords 
from . import db
from flask_login import login_required, login_user, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = None

        # Check if user is an employer
        employer = Employer.query.filter_by(email=email).first()
        if employer:
            if check_password_hash(employer.password, password):
                user = employer
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                #return redirect(url_for('views.seeker_home')) Do employer redirect
            else:
                flash('Incorrect email or password', category='error')

        # Check if user is an admin
        admin = Admin.query.filter_by(email=email).first()
        if admin:
            if check_password_hash(admin.password, password):
                user = admin
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                #return redirect(url_for('views.seeker_home')) Do admin redirect
            else:
                flash('Incorrect email or password', category='error')

        # Check if user is a job seeker
        job_seeker = User.query.filter_by(email=email).first()
        if job_seeker:
            if check_password_hash(job_seeker.password, password):
                user = job_seeker
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.seeker_home'))
            else:
                flash('Incorrect email or password', category='error')

        return render_template("login.html", user=current_user)
    else:
        return render_template('login.html', user=None)

@auth.route('/logout')
@login_required #can only access the logout function if a user is logged in. 
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST': 
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #checks if the email is already in use 
        user = Admin.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 6:
            flash('Email must be greater than 6 characters.', category='error') #flashes error message
        elif len(first_name) < 4:
            flash('First name must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 6:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            user = Admin(email=email, first_name=first_name, last_name=last_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)

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

        if len(email) < 6:
            flash('Email must be greater than 6 characters.', category='error') #flashes error message
        elif len(first_name) < 4:
            flash('First name must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 8:
            flash('Password must be greater than 8 characters.', category='error')
        else:
            user = User(email=email, first_name=first_name, last_name=last_name, phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.seeker_home'))
    return render_template("signup.html", user=current_user)

@auth.route('/signup_employer', methods=['GET', 'POST'])
def signup_employer():
    if request.method == 'POST': 
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        company_name = request.form.get('company_name')
        company_role = request.form.get('company_role')
        phone_number = request.form.get('phone_number')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #checks if the email is already in use 
        user = Employer.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 6:
            flash('Email must be greater than 6 characters.', category='error') #flashes error message
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 8:
            flash('Password must be greater than 8 characters.', category='error')
        else:
            user = Employer(first_name=first_name, last_name=last_name, email=email, company_name=company_name, company_role=company_role ,phone_number = phone_number, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True) #from flask_login, remembers that the user is logged in. Stored in session. 
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.employer_home'))
    return render_template("signup_employer.html", user=current_user)