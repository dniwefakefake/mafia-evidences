from flask import *

from back import api, load_evidences
from front import front

app = Flask(__name__)
app.register_blueprint(api)
app.register_blueprint(front)

if __name__ == '__main__':
    load_evidences()
    app.run()
