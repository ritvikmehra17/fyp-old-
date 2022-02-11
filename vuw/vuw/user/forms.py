# -*- coding: utf-8 -*-
"""User forms."""
from flask import render_template
from flask_wtf import FlaskForm
import werkzeug
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, regexp
from flask_wtf.file import FileField, TextAreaField
#from werkzeug import secure_filename
import os
import re

from .models import User


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired(), EqualTo("password", message="Passwords must match")],
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True


class UploadForm(FlaskForm):
    image        = FileField('Image File', [regexp('^[^/\\]\.jpg$')])
    #description  = TextAreaField('Image Description')

    def validate_image(form, field):
        if field.data:
            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

def upload(request):
    form = UploadForm(request.POST)
    if form.image.data:
        image_data = request.FILES[form.image.name].read()
        open(os.path.join("uploads", form.image.data), 'w').write(image_data)

    return render_template('upload.html', form=form) 


# class CubeForm(FlaskForm):
#     front_image= FileField('Image File', [regexp('^[^/\\]\.jpg$')])
#     back_image=FileField('Image File', [regexp('^[^/\\]\.jpg$')])
#     right_image=FileField('Image File', [regexp('^[^/\\]\.jpg$')])
#     left_image=FileField('Image File', [regexp('^[^/\\]\.jpg$')])
#     top_image=FileField('Image File', [regexp('^[^/\\]\.jpg$')])
#     bottom_image=FileField('Image File', [regexp('^[^/\\]\.jpg$')])

#     def validate_image(form, field):
#         if field.data:
#             field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

# def cube(request):
#     form = CubeForm(request.POST)
#     if form.image.data:
#         image_data = request.FILES[form.image.name].read()
#         open(os.path.join("uploads", form.image.data), 'w').write(image_data)

#     return render_template('cube.html', form=form)      