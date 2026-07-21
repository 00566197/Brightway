from wtforms.validators import ValidationError
import re
from datetime import date, time,datetime


import os

def strong_password(form, field):
    password=field.data
    if len(password)< 8:
        raise ValidationError('Password must be at least 8 characters long')
    if not re.search(r"[A-Z]",password):
        raise ValidationError('Passoword must Include an UpperCase letter')
    if not re.search(r"[a-z]",password):
        raise ValidationError('Password must include LowerCase letter')
    if not re.search(r"[\d]",password):
        raise ValidationError('Password must include at least a digit')
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]",password):
        raise ValidationError("Password must include special character")

    
def date_past(form, field):
    
    if field.data< date.today():
        raise ValidationError("Enter future Date, Date cant be in the past")
    
def working_time(form, field):
    timeer=field.data
    start=time(9,0)
    end=time(17,0)
    if timeer<start or timeer>end:
        raise ValidationError("We are not working during this hour pls pick a time between 9:00 to 17:00")


