#database models 

from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy 

#model for a job seeker 
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(15))
    resume_file = db.Column(db.LargeBinary)
    profile = db.Column(db.String(20)) #values are "seeker", "employer", "admin"
    Posts = db.relationship('Post', backref='user', passive_deletes=True)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    text = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(50))
    address = db.Column(db.String(50))
    salary = db.Column(db.Integer)
    field = db.Column(db.String(50)) #Example aerospace, programming etc
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author =db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)