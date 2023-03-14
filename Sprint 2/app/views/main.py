#This page is important to rander our html page on the web , so all routes are added here 
from flask import Blueprint, render_template, request,flash, redirect, url_for, send_file, make_response
from flask_login import login_required, current_user
from flask import Flask, render_template
from werkzeug.utils import secure_filename
from ..models import Post, User
from .. import db
from ..forms import ContactForm
import io


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

    return redirect (url_for('main.home'))

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
        '''if 'resume' not in request.files:
            flash('No file selected', category='error')
            return redirect(url_for('main.resume'))

        # Get the file object from the form
        resume_file = request.files['resume']
        if resume_file.filename == '':
            flash('No file selected', category='error')
            return redirect(url_for('main.resume'))

        if not allowed_file(resume_file.filename):
            flash('Invalid file type', category='error')
            return redirect(url_for('main.resume'))
       
        # Get the file contents as bytes
        resume_data = resume_file.read()
        # Save the file contents to the database as BLOB
        current_user.resume_file = resume_data
        db.session.commit()
        flash('Resume uploaded successfully!', category='success')
        '''
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
    return render_template('home/admin_home.html', user=current_user)

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