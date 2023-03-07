from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('portfolio1.config')

db = SQLAlchemy(app)  
from .models import account


import portfolio1.main