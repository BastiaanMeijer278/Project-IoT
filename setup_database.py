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
ijsberen = Diersoort('Ijsbeer')
db.session.add_all([ijsberen])

Henk = Dier('Ijsbeer', 'Henk', True, 'Nortica')
db.session.add_all([Henk])

db.session.commit()

witte_neushoorn = Diersoort('Witte neushoorn')
nijlpaard = Diersoort('Nijlpaard')
ringstaartmaki = Diersoort('Ringstaartmaki')
zuidelijke_pelsrob = Diersoort('Zuidelijke pelsrob')
bonte_vari = Diersoort('Bonte vari')
groene_zeeschildpad = Diersoort('Groene zeeschildpad')
sporenschildpad = Diersoort('Sporenschildpad')

db.session.add_all([witte_neushoorn, nijlpaard, ringstaartmaki, zuidelijke_pelsrob, bonte_vari, groene_zeeschildpad, sporenschildpad])

# Dieren = []
# verblijven = []
# for i in Verblijf.query.all():
#     verblijven += i.name

# for i in Diersoort.query.all():
#     for j in range(random.randint(3,5)):
#         Dieren += [Dier(i.name, names.get_first_name(), True, random.choice(verblijven))] 

Witte_neushoorn = Dier('Witte neushoorn', 'Witte neushond', True, 'Serenga')
Nijlpaard = Dier('Nijlpaard', 'Nijlpaard', True, 'Animazia')
Ringstaartmaki = Dier('Ringstaartmaki', 'Ringstaartmaki', False, 'Serenga')
Zuidelijke_pelsrob = Dier('Zuidelijke pelsrob', 'Zuidelijke pelsrob', True, 'Jungola')
Bonte_vari = Dier('Bonte vari', 'Bonte vari', True, 'Jungola')
Groene_zeeschildpad = Dier('Groene zeeschildpad', 'Groene zeeschildpad', True, 'Animazia')
Sporenschildpad = Dier('Sporenschildpad', 'Sporenschildpad', True, 'Animazia')



pieter = Dier('Nijlpaard', 'Pieter', False, 'Nortica')
db.session.add_all([pieter, Witte_neushoorn, Nijlpaard, Ringstaartmaki, Zuidelijke_pelsrob, Bonte_vari, Groene_zeeschildpad, Sporenschildpad])

db.session.commit()
