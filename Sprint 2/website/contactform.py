from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class ContactForm(FlaskForm):
  name = StringField("Name")
  email = StringField("Email")
  subject = StringField("Subject")
  message = TextAreaField("Message")
  submit = SubmitField("Send") 