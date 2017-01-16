from flask import *

import back

front = Blueprint("mafia_frontend", __name__, template_folder="templates")


@front.route("/")
def index():
    if len(back.evidences_cache) == 0:
        back.load_evidences()
    evidences = back.evidences_cache
    return render_template("index.html", evidences=evidences, keys=list(sorted(evidences.keys())))
