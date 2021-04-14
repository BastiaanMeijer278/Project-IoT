from Webapplicatie import db, Verblijf
from Webapplicatie.models import *
import random
import names

db.create_all()

serenga = Verblijf('Serenga')
jungola = Verblijf('Jungola')
nortica = Verblijf('Nortica')
animazia = Verblijf('Animazia')

db.session.add_all([serenga, jungola, nortica, animazia])
ijsberen = Diersoort('Ijsbeer', 'Nortica')
db.session.add_all([ijsberen])

Henk = Dier('Ijsbeer', 'Henk', True)
db.session.add_all([Henk])

db.session.commit()

witte_neushoorn = Diersoort('Witte neushoorn', 'Serenga')
nijlpaard = Diersoort('Nijlpaard', 'Serenga')
ringstaartmaki = Diersoort('Ringstaartmaki', 'Jungola')
zuidelijke_pelsrob = Diersoort('Zuidelijke pelsrob', 'Nortica')
bonte_vari = Diersoort('Bonte vari', 'Jungola')
groene_zeeschildpad = Diersoort('Groene zeeschildpad', 'Animazia')
sporenschildpad = Diersoort('Sporenschildpad', 'Animazia')

db.session.add_all([witte_neushoorn, nijlpaard, ringstaartmaki, zuidelijke_pelsrob, bonte_vari, groene_zeeschildpad, sporenschildpad])

Dieren = []
for i in Diersoort.query.all():
    for j in range(random.randint(3,5)):
        Dieren += [Dier(i.name, names.get_first_name(), True)] 


db.session.add_all(Dieren)

pieter = Dier('Nijlpaard', 'Pieter', False)
db.session.add_all([pieter])

db.session.commit()





# db.session.add_all([ijsberen])
# db.session.commit