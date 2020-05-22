from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flaskapp.models import User



class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField(label='Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField(label='Register')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already take.")



class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember = BooleanField(label='Remember me')
    submit = SubmitField(label='Login')



class PostForm(FlaskForm):
    content = TextAreaField(label='Content', validators=[
        DataRequired()
    ])
    submit = SubmitField(label='Post')