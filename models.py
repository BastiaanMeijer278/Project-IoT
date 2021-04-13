import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'd42cee127ae26605af73cc0365302fc5'

class Verblijf(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

class Dier(db.model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    detected = db.Column(db.Boolean)
    verblijf = db.Column(db.Integer,db.Foreignkey("Verblijf.id"))
    
class Sensor(db.model):
    id = db.Column(db.Integer, primary_key = True)
    output = db.Column(db.Text)
    dier = db.Column(db.Text,db.Foreignkey("Dier.id"))