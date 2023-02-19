#This page is important to rander our html page on the web , so all routes are added here 
from flask import Blueprint, render_template, request,flash, redirect, url_for
from flask_login import login_required, current_user
from flask import Flask, render_template
from .models import Post
from. import db


views = Blueprint('views', __name__)

@views.route('/') 
def home():
    posts = Post.query.all()
    return render_template("base.html", user=current_user, posts=posts)  #renders the HTML inside the home.html file

@views.route('/seeker_home')
@login_required
def seeker_home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    print(current_user)
    return render_template("seeker_home.html", user=current_user)

@views.route('/employer_home')
@login_required
def employer_home():
    return render_template("employer_home.html", user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route("/create-post", methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        text= request.form.get('text')

        if not text:
            flash('Post cannot be empty', category ='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created',category ='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html',user=current_user)

