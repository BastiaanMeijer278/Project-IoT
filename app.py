from Webapplicatie import app, db, message
from Webapplicatie.models import *
from flask import render_template


@app.route('/')
def index():
    residences = Verblijf.query.all()
    animals = Dier.query.all()
    
    d = {}
    missing_animals = {}
    for i in residences:
        d[i.id] = []
        missing_animals[i.id] = []
        # print(missing_animals.keys())
        soort = Dier.query.filter_by(verblijf=i.id).all()
        L = [k for k in soort if k.detected == False]
        for k in Dier.query.filter_by(verblijf=i.id, detected=False).all():
            print(i.id)
            if k.detected == False and k is not None:
                missing_animals[i.id] += [k]
                pushmsg = message.SendPushNotification(k.name, i.name)
                pushmsg.Send()
        print(missing_animals)

        for j in soort:
            d[i.id] += [k for k in animals if k.id == j.id and k.detected == True]


    soorten = {}
    for i in Diersoort.query.all():
        soorten[i.id] = ''
        soorten[i.id] += i.name

    return render_template('home.html', residence=residences, list_of_animals=d, soorten=soorten, missing_animals=missing_animals)

if __name__ == '__main__':
    app.run(debug=True)
