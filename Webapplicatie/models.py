import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'd42cee127ae26605af73cc0365302fc5'

class Verblijf(db.Model):

    __tablename__ = "Verblijf"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Diersoort(db.Model):

    __tablename__ = "Diersoort"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)
    verblijf = db.Column(db.Integer,db.ForeignKey("Verblijf.id"))

    def __init__(self, name, verblijf):
        self.name = name
        self.verblijf = verblijf

class Device(db.Model):

    __tablename__ = "Device"
    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.Text)

    def __init__(self, address):
        self.address = address
    
class Dier(db.Model):

    __tablename__ = "Dier"
    id = db.Column(db.Integer, primary_key = True)
    soort = db.Column(db.Integer, db.ForeignKey("Diersoort.id"))
    name = db.Column(db.Text)
    device = db.Column(db.Integer, db.ForeignKey("Device.id"))
    detected = db.Column(db.Boolean)

    def __init__(self, soort, name, device, detected):
        self.soort = soort
        self.name = name
        self.device = device
        self.detected = detected

class Sensor(db.Model):

    __tablename__ = "Sensor"
    id = db.Column(db.Integer, primary_key = True)
    verblijf = db.Column(db.Integer, db.ForeignKey("Verblijf.id"))

    def __init__(self, verblijf):
        self.verblijf = verblijf

class Data(db.Model):

    __tablename__ = "Data"
    id = db.Column(db.Integer, primary_key = True)
    sensor = db.Column(db.Integer, db.ForeignKey("Sensor.id"))
    dier = db.Column(db.Integer,db.ForeignKey("Dier.id"))
    output = db.Column(db.Text)

    def __init__(self, sensor, dier, output):
        self.sensor = sensor
        self.dier = dier
        self.output = output
        