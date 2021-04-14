from Webapplicatie import app, db
from Webapplicatie.models import *
from flask import render_template

@app.route('/')
def index():
    residences = Verblijf.query.all()
    animals = Dier.query.all()
    
    d = {}
    for i in residences:
        d[i.id] = []
        soort = Diersoort.query.filter_by(verblijf=i.id).all()
        for j in soort:
            d[i.id] += [k for k in animals if k.soort == j.id and k.detected == True]
            if Dier.query.filter_by(soort=j.id, detected=False).all():
                alarm = True
            else:
                alarm = False

    soorten = {}
    for i in Diersoort.query.all():
        soorten[i.id] = ''
        soorten[i.id] += i.name

    return render_template('home.html', residence=residences, list_of_animals=d, soorten=soorten, alarm=alarm)

if __name__ == '__main__':
    app.run(debug=True)