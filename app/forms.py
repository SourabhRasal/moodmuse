from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('doctor', 'Doctor'), ('admin', 'Admin')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PatientForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150)])
    gender = SelectField('Gender', choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()], widget=TextArea())
    submit = SubmitField('Save Patient')

class VisitForm(FlaskForm):
    date = DateTimeField('Visit Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    symptoms = TextAreaField('Symptoms', validators=[DataRequired()], widget=TextArea())
    prescription = TextAreaField('Prescription', validators=[Optional()], widget=TextArea())
    follow_up_required = BooleanField('Follow-up Required')
    follow_up_date = DateField('Follow-up Date', validators=[Optional()])
    notes = TextAreaField('Additional Notes', validators=[Optional()], widget=TextArea())
    submit = SubmitField('Save Visit')