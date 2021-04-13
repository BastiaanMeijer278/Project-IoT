from flask_sqlalchemy import *
from Webapplicatie import db

class Verblijf(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Dier(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    detected = db.Column(db.Boolean)
    verblijf = db.Column(db.Integer)
    
class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    output = db.Column(db.Text)
    dier = db.Column(db.Text)