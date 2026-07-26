import os
from dotenv import load_dotenv

load_dotenv()


load_dotenv()  # reads .env file locally; no-op on Render

DATABASE_URL = os.environ.get("DATABASE_URL")
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or'sqlite:///' + os.path.join(basedir,'app.db')
    UPLOAD_FOLDER=os.path.join(basedir,'static','videos') ## this is going to be used for videos uploads 