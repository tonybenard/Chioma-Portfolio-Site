from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    name = StringField("Full name", [DataRequired()])
    email = EmailField("Email address", [DataRequired(), Email()]) 
    mobile = StringField("Phone number", [DataRequired()])
    msg = TextAreaField("Message", [DataRequired()])
    submit = SubmitField("submit")