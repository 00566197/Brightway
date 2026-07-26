from wtforms import *
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Optional,NumberRange
from flask_wtf import FlaskForm
from app import db
from app.models import *
import sqlalchemy as sa
from app.validators import *
from flask_wtf.file import FileField,FileAllowed,FileRequired 

class CarUpload(FlaskForm):
    car_name=StringField('Car Name',validators=[DataRequired()],render_kw={'placeholder':'The Car Name'})
    car_model=StringField('Car Model',validators=[DataRequired()],render_kw={'placeholder':'The Car Model'})
    car_year=StringField('Car Year',validators=[DataRequired()],render_kw={'placeholder':'The Car Release Date'})
    horse_power=IntegerField('Car Horse Power',validators=[DataRequired()],render_kw={'placeholder':'Car Horse Power'})
    top_speed=IntegerField('Car Top Speed',validators=[DataRequired()],render_kw={'placeholder':'Car Top Speed'})
    rating=rating = IntegerField(' Car Rating (1-5)', validators=[
        DataRequired(message="Please provide a rating"),
        NumberRange(min=1, max=5, message="Rating must be between 1 and 5")
    ])
    car_color=StringField('Car Color',validators=[DataRequired()],render_kw={'placeholder':'The Car Color'})
    availability=SelectField('Availability',choices=[('available','Available'),('limited','Limited Stock'),('sold','Sold')])
    car_price=FloatField('Car Price',validators=[DataRequired()],render_kw={'placeholder':'Car Price'})
    car_type=SelectField('Car Type',choices=[('new','New'),('used','Used'),('fixed','Fixed')])
    information=TextAreaField('Car Detailed Information',validators=[DataRequired()],render_kw={'placeholder':'Information Needed By The Customer'})
    images=MultipleFileField('Car Images',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'img','webp'],'Images Only')])
    submit=SubmitField('Submit')


class MessageUs(FlaskForm):
    f_name=StringField('First Name',validators=[DataRequired()])
    l_name=StringField('Last Name',validators=[DataRequired()])
    email=EmailField('Email Address',validators=[DataRequired(),Email()])
    phone_number=StringField('Phone Number',validators=[Optional()])
    enquiry_type=SelectField('Select an enquiry type',choices=[('vehicle enquiry','Vehicle Enquiry'),('test drive request', 'Test Drive Request'),('finance enquiry','Finance Enquiry'),('part exchange','Part Exchange'),('general query','General Query')])
    message=TextAreaField('Message',validators=[DataRequired()])
    submit=SubmitField('Submit')


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Submit')