from Webapplicatie import db, Verblijf
from Webapplicatie.models import *

db.create_all()

savannenhuis = Verblijf('Savannenhuis')
serenga = Verblijf('Serenga')
jungola = Verblijf('Jungola')
nortica = Verblijf('Nortica')
animazia = Verblijf('Amimazia')

db.session.add_all([savannenhuis, serenga, jungola, nortica, animazia])
db.session.commit()
