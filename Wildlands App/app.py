from Webapplicatie import app, db, message
from Webapplicatie.models import *
from Webapplicatie.forms import *
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, redirect, url_for, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
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
                # pushmsg.Send()
        print(missing_animals)

        for j in soort:
            d[i.id] += [k for k in animals if k.id == j.id and k.detected == True]


    soorten = {}
    for i in Diersoort.query.all():
        soorten[i.id] = ''
        soorten[i.id] += i.name

    return render_template('home.html', residence=residences, list_of_animals=d, soorten=soorten, missing_animals=missing_animals)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('dashboard')
                return redirect(next)
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = register_form()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    tel=form.tel.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    admin = current_user.admin
    stays = Verblijf.query.all()
    animals = Dier.query.all()
    sort = Diersoort.query.all()
    change_pw = change_password()
    addstay = add_stay()
    addanimal = add_animal()
    if change_pw.validate_on_submit():
        print('hoi')
        user = User.query.get(current_user.id)
        print(user)
        user.password = change_pw.password.data
        db.session.add(user)
        db.session.commit()
        print('Mooiman')
        return redirect(url_for('dashboard'))
    elif addstay.validate_on_submit():
        stay = Verblijf(addstay.stay.data)
        db.session.add(stay)
        db.session.commit()
        return redirect(url_for('panel'))
    elif addanimal.validate_on_submit():
        animal = Dier(addanimal.soort.data, addanimal.naam.data, False, addanimal.device.data, addanimal.verblijf.data)
        db.session.add(animal)
        db.session.commit()
        return redirect(url_for('panel'))
    return render_template('panel.html', admin=admin, change_pw=change_pw, stays=stays, addstay=addstay, animals=animals, addanimal=addanimal, sort=sort)

@app.route('/rem_stay/<id>')
@login_required
def rem_stay(id):
    stay = Verblijf.query.get(id)
    db.session.delete(stay)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/rem_animal/<id>')
@login_required
def rem_animal(id):
    dier = Dier.query.get(id)
    db.session.delete(dier)
    db.session.commit()
    return redirect(url_for('panel'))

@app.route('/rem_sort/<id>')
@login_required
def rem_sort(id):
    sort = Diersoort.query.get(id)
    db.session.delete(sort)
    db.session.commit()
    return redirect(url_for('panel'))

if __name__ == '__main__':
    app.run(debug=True)