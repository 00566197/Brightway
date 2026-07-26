from sqlalchemy import Column,Float, Integer,VARCHAR, Date, String, DateTime, ForeignKey, Table, Time,Enum
from sqlalchemy.orm import relationship
from app import db, login
from datetime import datetime, timezone
import hashlib
from flask_login import UserMixin
from app.types import Roles

@login.user_loader
def load_user(id):
    return staff_user
class StaffUser(UserMixin):
    id=1

staff_user=StaffUser()


class Car(db.Model):
    __tablename__='cars'

    id=Column(Integer,primary_key=True)
    car_name=Column(String)
    car_model=Column(String)
    car_year=Column(String)
    horse_power=Column(Integer)
    top_speed=Column(Float)
    rating=Column(Float)
    car_color=Column(String)
    availability=Column(String)
    car_price=Column(Float)
    car_type=Column(String)
    information=Column(String)
    images=relationship('CarImages',
                        backref='car',
                        lazy=True)
    def __init__(self,car_name, car_model,car_year,horse_power,
                 top_speed,rating,car_color,availability,car_price,car_type,information):
        self.car_name=car_name
        self.car_model=car_model
        self.car_year=car_year
        self.horse_power=horse_power
        self.top_speed=top_speed
        self.rating=rating
        self.car_color=car_color
        self.availability=availability
        self.car_price=car_price
        self.car_type=car_type
        self.information=information
class CarImages(db.Model):
    __tablename__='car_images'

    id=Column(Integer,primary_key=True)
    image_filename=Column(String,nullable=False)
    car_id=Column(Integer,ForeignKey(Car.id))


    

class Message(db.Model):
    __tablename__='messages'
    id=Column(Integer,primary_key=True)

    f_name=Column(String)
    l_name=Column(String)
    email=Column(String)
    phone_number=Column(String)
    enquiry_type=Column(String)
    message=Column(String)
    is_read=Column(String,default='unread')
    def __init__(self,f_name,l_name,email,phone_number,enquiry_type,message):
        self.f_name=f_name
        self.l_name=l_name
        self.email=email
        self.phone_number=phone_number
        self.enquiry_type=enquiry_type
        self.message=message