from flask import *
from message import *


app = Flask(__name__)


@app.route('/')
def index():
    residences = ['Savannenhuis', 'Serenga', 'Jungola', 'Nortica', 'Animazia']
    return render_template('home.html', residence=residences)

if __name__ =='__main__':
    app.run(debug=True)