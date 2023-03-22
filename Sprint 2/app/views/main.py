#This page is important to rander our html page on the web , so all routes are added here 
from flask import Blueprint, render_template, request,flash, redirect, url_for, send_file, make_response
from flask_login import login_required, current_user
from flask import Flask, render_template
from werkzeug.utils import secure_filename
from ..models import Post, User, Application, Notification
from .. import db
from ..forms import ContactForm
import io
from datetime import datetime


main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/') #insert URL here
def home():
    posts = Post.query.all()
    return render_template("home/home.html", user=current_user, posts=posts)  #renders the HTML inside the home.html file

@main.route('/overview', methods=['GET', 'POST'])
def overview():
    if current_user.profile == 'employer':
        return redirect(url_for('main.employer_home'))
    elif current_user.profile == 'seeker':
        return redirect(url_for('main.seeker_home'))
    elif current_user.profile == 'admin':
        return redirect(url_for('main.admin_home'))
    return render_template('home/overview.html')


@main.route('/seeker_home')
@login_required
def seeker_home():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return render_template("home/seeker_home.html", user=current_user)

@main.route('/employer_home')
@login_required
def employer_home():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return render_template("home/employer_home.html", user=current_user)

@main.route('/about')
def about():
    return render_template('about.html', user=current_user)

@main.route("/create_post", methods=['GET','POST'])
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
            post = Post(text=text, title=title, company=company, address=address, salary=salary, field=field, author_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created',category ='success')
            return redirect(url_for('main.home'))

    return render_template('create_post.html',user=current_user)

@main.route("/jobposting", methods=['GET', 'POST'])
def jobposting():
    posts = Post.query.all()
    print(posts)
    return render_template("jobposting.html", user=current_user, posts=posts)

@main.route("/myposts", methods=['GET', 'POST'])
def myposts():
    posts = Post.query.filter_by(author=current_user.id).all()
    print(posts)
    return render_template("myposts.html", user=current_user, posts=posts)

@main.route("/editpost/<id>", methods = ['POST', 'GET'])
@login_required
def editpost(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        post.title = request.form['title']
        post.text = request.form['text']
        db.session.commit()
        return redirect(url_for('main.myposts'))
    return render_template('editpost.html', post=post, user=current_user)

@main.route("/editinfo/<id>", methods = ['POST', 'GET'])
@login_required
def editinfo(id):
    user = User.query.filter_by(id=id).first()
    if request.method == 'POST':
        if user.profile == 'seeker':
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
           # user.password = request.form['password']
            db.session.commit()
            return redirect(url_for('main.seeker_home'))
        if user.profile == 'employer':
            user.email = request.form['email']
            user.phone_number = request.form['phone_number']
            #user.password = request.form['password']
            db.session.commit()
            return redirect(url_for('main.employer_home'))
    return render_template('editinfo.html', user=current_user)



@main.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash ("Post does not exist.", category='error')

    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='success')

    return redirect (url_for('main.home'), user=current_user)

@main.route("/apply-post/<id>", methods=['GET', 'POST'])
@login_required
def apply_post(id):
    post = Post.query.filter_by(id=id).first()
    if request.method == 'POST':
        application = Application()
        application.user_id = current_user.id
        application.post_id = id
        application.author_num = post.author_id
        application.applicant_name = current_user.first_name
        application.applicant_resume = current_user.resume_file
        application.title = post.title
        application.date_applied = datetime.utcnow()
        # Get the file object from the form
        resume = request.files['resume_file']
        # Get the file contents as bytes
        resume_data = resume.read()
        # Save the file contents to the database as BLOB
        application.applicant_resume = bytes(resume_data)
        flash('Resume uploaded successfully!', category='success')
        
        application.resume_file = request.files['resume_file'].read()
        db.session.add(application)
        
        message = f'{current_user.first_name} {current_user.last_name} has applied to your job post: {post.title}'

        notification = Notification(message=message, user_id=post.author_id)
        db.session.add(notification)
        db.session.commit()

        flash('Your application has been submitted.')
        return redirect(url_for('main.admin_home', notification=notification, post=post, user=current_user))
    return render_template('apply_post.html', post=post, notification=notification, user=current_user)

@login_required
@main.route('/applications', methods=['GET', 'POST'])
def applications_review():
    applications = Application.query.filter_by(author_num=current_user.id).all()
    post = None  # Initialize post to None

    return render_template('test_apply.html', post=post, applications=applications, user=current_user)

@login_required
@main.route('/notifications', methods=['GET', 'POST'])
def notifications_page():
    applications = Application.query.filter_by(author_num=current_user.id).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).all()
    post = None  # Initialize post to None

    return render_template('notifications.html', post=post, applications=applications, notifications=notifications, user=current_user)

@main.route('/contact-applicant/<string:applicant_name>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def contact_applicant(applicant_name, post_id):
    # Find the user with the specified name
    user = User.query.filter_by(first_name=applicant_name).first()
    post = Post.query.filter_by(id=post_id)
    
    if user:
        # Send a notification to the user
        message = "You've been contacted by {} about your application.".format(current_user.first_name)
        notification = Notification(message=message, user_id=user.id)
        db.session.add(notification)
        db.session.commit()
        
        flash("Your message has been sent to {}.".format(applicant_name))
    else:
        flash("Couldn't find a user with the name {}.".format(applicant_name))
    
    return redirect(url_for('main.applications_review', user=current_user))

@main.route('/refuse-applicant/<string:applicant_name>/<int:post_id>', methods=['GET', 'POST'])
@login_required
def refuse_applicant(applicant_name, post_id):
    # Find the user with the specified name
    user = User.query.filter_by(first_name=applicant_name).first()
    post = Post.query.filter_by(id=post_id).first()
    
    if user:
        # Send a notification to the user
        message = "Unfortunately your application has not been retained at the moment for the {} position at {}.".format(post.title, current_user.company_name)
        notification = Notification(message=message, user_id=user.id)
        db.session.add(notification)
        db.session.commit()
        
        flash("Your message has been sent to {}.".format(applicant_name))
    else:
        flash("Couldn't find a user with the name {}.".format(applicant_name))
    
    return redirect(url_for('main.applications_review', user=current_user))


@login_required
def get_notifications():
    if current_user:
        notifications = Notification.query.filter_by(user_id=current_user.id).all()
        return notifications
    else:
        return []

@main.context_processor
def inject_notifications():
    notifications = get_notifications()
    return dict(notifications=notifications)

@main.route("/posts/<username>")
@login_required
def posts(username):
    user = user.query.filter_by(username=username).first()

    if not user:
        flash('No user wih that username exists.', category='error')
        return redirect(url_for('main.home'))

    post = Post.query.filter_by(author_id=user.id).all()
    return render_template("posts.html", user=current_user, posts= post,username=username )

@main.route('/search', methods=['GET', 'POST'])
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

    return redirect(url_for('main.jobposting'))

@main.route('/resume', methods=['GET', 'POST'])
@login_required
def resume():
    if request.method == 'POST':
        if request.method == 'POST':
            # Get the file object from the form
            resume = request.files['resume']
            # Get the file contents as bytes
            resume_data = resume.read()
            # Save the file contents to the database as BLOB
            current_user.resume_file = bytes(resume_data)
            db.session.commit()
            flash('Resume uploaded successfully!', category='success')
        else:
            flash('Resume not uploaded successfully!', category='error')

        return render_template('resume.html', user=current_user)


    return render_template('resume.html', user=current_user)

@main.route('/download_resume')
@login_required
def download_resume():
    # Get the resume file from the database for the current user
    resume_file = current_user.resume_file

    # Send the file as a response to the user's request
    return send_file(
        io.BytesIO(resume_file),
        mimetype='application/pdf',
        as_attachment=False
    )


@main.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    #TODO decide which elements we should be able to affect
    return render_template('settings.html', user=current_user)

@main.route('/help', methods=['GET', 'POST'])
def help():
    #TODO make a contact us page 
    return render_template('help.html')

@main.route('/admin_home', methods=['GET', 'POST'])
@login_required
def admin_home():
    notifications = get_notifications()
    return render_template('home/admin_home.html', user=current_user, notifications=notifications)

@main.route('/contact-us', methods = ['GET','POST'])
def contact():
  form = ContactForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('/contact.html', form=form)
    else:
      return 'Form posted.'
  elif request.method == 'GET':
    return render_template('/contact.html', form=form)