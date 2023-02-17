from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import Flask, render_template

views = Blueprint('views', __name__)

@views.route('/') #insert URL here
def home():
    return render_template("home.html", user=current_user)  #renders the HTML inside the home.html file

@views.route('/seeker_home')
@login_required
def seeker_home():
    return render_template("seeker_home.html", user=current_user)

@views.route('/employer_home')
@login_required
def employer_home():
    return render_template("employer_home.html", user=current_user)

@views.route('/about')
def about():
    return render_template('about.html')