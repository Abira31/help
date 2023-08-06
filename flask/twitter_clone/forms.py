from flask_wtf import FlaskForm
from wtforms import StringField,FileField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import InputRequired,Length



class RegisterForm(FlaskForm):
    name = StringField('Full name',validators=[InputRequired('A full name is required.'),Length(max=100)])
    username = StringField('Username',validators=[InputRequired('Username is required.'),Length(max=100)])
    password = PasswordField('Password',validators=[InputRequired('A password is required')])
    image = FileField(validators=[InputRequired('A password is image')])

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired('Username is required.'),Length(max=30)])
    password = PasswordField('Password',validators=[InputRequired('A password is required')])
    remember = BooleanField('Remember me')

class TweetForm(FlaskForm):
    text = TextAreaField('Message',validators=[InputRequired('Message is required')])