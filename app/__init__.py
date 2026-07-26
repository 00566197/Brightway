from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app=Flask(__name__)
app.config.from_object(Config)
Bootstrap5(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)
login=LoginManager(app)
login.login_view='staff_login'
login.login_message='Please Log in to access this page'

## this code below wil be used for the succesful video upload and storage 
UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
# the code below will be used to automatically create video file if a video is to be added 
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
from app import routes,models