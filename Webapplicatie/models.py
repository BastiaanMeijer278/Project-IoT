from Webapplicatie import db

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
        self.verblijf = Verblijf.query.filter_by(name=verblijf).first().id
    
class Dier(db.Model):

    __tablename__ = "Dier"
    id = db.Column(db.Integer, primary_key = True)
    soort = db.Column(db.Integer, db.ForeignKey("Diersoort.id"))
    name = db.Column(db.Text)
    detected = db.Column(db.Boolean)

    def __init__(self, soort, name, detected):
        self.soort = Diersoort.query.filter_by(name=soort).first().id
        self.name = name
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
    dier = db.Column(db.Text,db.ForeignKey("Dier.id"))
    output = db.Column(db.Text)

    def __init__(self, sensor, dier, output):
        self.sensor = sensor
        self.dier = dier
        self.output = output