#This page is important to rander our html page on the web , so all routes are added here 
from flask import Blueprint, render_template, request,flash, redirect, url_for
from flask_login import login_required, current_user
from flask import Flask, render_template
from .models import Post, User
from. import db


views = Blueprint('views', __name__)

@views.route('/') #insert URL here
@views.route('/home') 
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)  #renders the HTML inside the home.html file

@views.route('/seeker_home')
@login_required
def seeker_home():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return render_template("seeker_home.html", user=current_user)

@views.route('/employer_home')
@login_required
def employer_home():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return render_template("employer_home.html", user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route("/create_post", methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        text= request.form.get('text')
        title=request.form.get('title')
        address = "Chicago IL"
        field = "AeroSpace"
        salary = 25000
        
        company = current_user.company_name
        
        if not text:
            flash('Post cannot be empty', category ='error')
        else:
            post = Post(text=text, title=title, company=company, address=address, salary=salary, field=field, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created',category ='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html',user=current_user)

@views.route("/jobposting", methods=['GET', 'POST'])
def jobposting():
    posts = Post.query.all()
    print(posts)
    return render_template("jobposting.html", user=current_user, posts=posts)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash ("Post does not exist.", category='error')

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect (url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = user.query.filter_by(username=username).first()

    if not user:
        flash('No user wih that username exists.', category='error')
        return redirect(url_for('views.home'))

    post = Post.query.filter_by(author=user.id).all()
    return render_template("posts.html", user=current_user, posts= post,username=username )

@views.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        what = request.form['what']
        where = request.form['where']

        if what or where:
            # Query the posts that match the what and where conditions
            posts = Post.query.filter(Post.title.like(f'%{what}%'), Post.address.like(f'%{where}%')).all()

            if not posts:
                flash('No job postings found.', category='error')

            return render_template('jobposting.html', posts=posts)

        else:
            flash('Please enter search criteria.', category='error')

    return redirect(url_for('views.jobposting'))