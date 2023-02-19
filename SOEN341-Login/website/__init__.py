from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



db = SQLAlchemy() #sets up the db. database variable is db
DB_NAME = "database.sqlite" #the name of the database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skey1'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #db is located in the website folder
    db.init_app(app) #initialized db with the current app 



    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #import models file to define the classes before creating the db
    from .models import User, Note, Employer, Post, Admin
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #redirects to this page if a user tries to access a page that requires login.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Check if user exists in Employer table
        user = Employer.query.get(int(id))
        if user:
            return user
        # If user not found in Employer table, check if user exists in Admin table
        user = Admin.query.get(int(id))
        if user:
            return user
        user = User.query.get(int(id))
        if user:
            return user
        # If user not found in either table, return None
        return None
            
    with app.app_context():
        db.create_all()
    # create_database(app)

    return app

def create_database(app): #checks if the db exists, and if not, creates it
    if not path.exists('website/' + DB_NAME): #website folder 
        db.create_all(app=app)
        print('Database created.')

