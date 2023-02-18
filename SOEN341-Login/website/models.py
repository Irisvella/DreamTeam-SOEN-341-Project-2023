#database models 

from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy 
#test note class from tutorial 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #associates the note to the user that created it

class Employer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    company_name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

#model for a job seeker 
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(15))
    profile = db.Column(db.String(20)) #determines if the user is a job seeker, employer, or admin 
    notes = db.relationship('Note') #everytime a note is created, the note id is stored here.
    Posts = db.relationship('Post', backref='user', passive_deletes=True)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author =db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)