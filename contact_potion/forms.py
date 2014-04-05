from flask_wtf import Form
from wtforms.fields.html5 import EmailField
from wtforms.fields import (
    TextField,
    TextAreaField,
    SubmitField,
    SelectField
)
from wtforms.validators import DataRequired, Email


class ContactForm(Form):
    name = TextField("Name",
                     validators=[DataRequired("Please enter your name")])
    email = EmailField("Email",
                       validators=[
                           DataRequired("Please enter your email address"),
                           Email("Please enter a valid email address")])
    category = SelectField("Category",
                           choices=[
                               ('quote', 'Request a Quote'),
                               ('feedback', 'Website Feedback')
                           ],
                           validators=[DataRequired()])
    subject = TextField("Subject",
                        validators=[DataRequired(
                            "Please enter a subject line for the message")])
    message = TextAreaField("Message",
                            validators=[DataRequired("Please enter a message")])
    submit = SubmitField("Send")
