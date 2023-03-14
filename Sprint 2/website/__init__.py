from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail

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

    #mail smtp initializaton
    mail = Mail()
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = 'findagoodjob101@gmail.com'
    #app password, real password is goodjob123
    app.config["MAIL_PASSWORD"] = 'lswcxksinkcjojuc'
    mail.init_app(app)

    #import models file to define the classes before creating the db
    from .models import User, Post
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #redirects to this page if a user tries to access a page that requires login.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    create_database(app)

    return app
import importlib
from sqlalchemy.engine import reflection
from sqlalchemy.exc import NoSuchTableError

def create_database(app):
    with app.app_context():
        db.create_all()

        # Import all models from models.py file
        models = []
        module = importlib.import_module('.models', package='website')
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, db.Model):
                models.append(obj)

        # Check if any models have changed
        inspector = reflection.Inspector.from_engine(db.engine)
        for model in models:
            table_name = model.__tablename__
            try:
                columns = [c['name'] for c in inspector.get_columns(table_name)]
            except NoSuchTableError:
                db.create_all()
                print(f'{table_name} table created.')
                continue

            expected_columns = [c.name for c in model.__table__.columns]
            if set(columns) != set(expected_columns):
                db.drop_all()
                db.create_all()
                print(f'{table_name} table recreated.')
