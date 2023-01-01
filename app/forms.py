from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        description="enter username",
        validators=[
            DataRequired(),
        ],
    )
    email = EmailField(
        label="Email",
        description="enter email address",
        validators=[DataRequired(), Email(message="not a valid email")],
    )
    password = PasswordField(
        label="Password",
        description="enter password",
        validators=[
            DataRequired(),
            Length(min=8, message="password should of min length 8"),
        ],
    )
    profile_pic = FileField(
        label="Profile pic",
        description="choose profile pic",
        validators=[DataRequired()],
    )
    register = SubmitField(label="Register")


class PostForm(FlaskForm):
    title = StringField(
        label="Title", description="Enter title for post", validators=[DataRequired()]
    )
    content = StringField(
        label="Content",
        description="Enter content for post",
        validators=[DataRequired()],
    )
    post = SubmitField(label="Post")
