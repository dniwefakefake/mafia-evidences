import random

import redis as r_
from flask import *

api = Blueprint("mafia_api", __name__, template_folder="templates")
evidences_cache = {}
redis = r_.StrictRedis(host='localhost', port=6379, db=0)


def load_evidences():
    global evidences_cache
    f1 = open("evidences.json", encoding="utf-8").read()
    evidences_cache = json.loads(f1)


# unsafe af, lol
def build_custom_checker(evidence):
    lambda_text = "lambda %s: %s" % (evidence["checker_variable"], evidence["checker_code"])
    lambda_f = eval(lambda_text)
    return lambda_f


def check_evidence(id, evidence, attempt):
    if evidence["checker"] not in ["oneOf", "custom"]:
        return '["error": "checker not found"]'

    if "case_sensitive" not in evidence:
        evidence["case_sensitive"] = True

    if evidence["checker"] == "oneOf":
        if not evidence["case_sensitive"] and attempt in evidence["answers"]:
            return evidence["hint"]
        elif evidence["case_sensitive"] and attempt.lower() in map(str.lower, evidence["answers"]):
            return evidence["hint"]
    elif evidence["checker"] == "custom":
        checker = build_custom_checker(evidence)
        if checker(attempt):
            return evidence["hint"]

    if not evidence["case_sensitive"]:
        attempt = attempt.lower()

    redis_path = "attempt:%s:%s" % (id, attempt)
    if not redis.exists(redis_path):
        redis.set(redis_path, random.choice(evidence["possible_hints"]))
    return redis.get(redis_path)


@api.route("/api/evidence/feedback/<id>/<attempt>")
def evidence_feedback(id, attempt):
    if len(evidences_cache) == 0:
        load_evidences()

    if id not in evidences_cache:
        return '["error": "evidence not found"]'

    result = check_evidence(id, evidences_cache[id], attempt)
    return result
