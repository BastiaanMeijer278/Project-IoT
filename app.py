from Webapplicatie import app, db
from Webapplicatie.models import *
from flask import render_template

@app.route('/')
def index():
    residences = Verblijf.query.all()
    return render_template('home.html', residence=residences)

if __name__ =='__main__':
    app.run(debug=True)