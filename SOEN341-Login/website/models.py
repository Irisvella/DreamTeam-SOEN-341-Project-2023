#database models 

from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

#test note class from tutorial 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user_seeker.id')) #associates the note to the user that created it

class Employer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    company_name = db.Column(db.String(50), unique=True)
    passowrd = db.Column(db.String(50))

#model for a job seeker 
class User_seeker(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    first_name = db.Column(db.String(50))
    notes = db.relationship('Note') #everytime a note is created, the note id is stored here.