from portfolio1 import db
from datetime import datetime


class Account(db.Model):
    __tablename__ = 'account'
    number = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    name = db.Column(db.String(15))  
    id = db.Column(db.String(24))  
    password = db.Column(db.String(24)) 