from fuzzywuzzy import fuzz
from data import OFFICIAL_APP
from difflib import SequenceMatcher

# 1) Name similarity
def name_similarity(app):
    official_name = OFFICIAL_APP["name"]
    candidate_name = app["name"]
    return fuzz.token_set_ratio(official_name, candidate_name)  # 0–100

# 2) Package similarity
def package_similarity(app):
    official_pkg = OFFICIAL_APP["package"]
    cand_pkg = app["package"]
    ratio = SequenceMatcher(None, official_pkg, cand_pkg).ratio()  # 0–1
    return round(ratio * 100, 2)

# 3) Publisher match
def publisher_match(app):
    official_pub = OFFICIAL_APP["publisher"].strip().lower()
    cand_pub = app["publisher"].strip().lower()
    return official_pub == cand_pub

# 4) Text suspicion
SUSPICIOUS_KEYWORDS = [
    "free", "bonus", "earn", "reward", "cashback", "double money",
    "lottery", "trick", "hack", "win", "prize"
]

def text_suspicion_score(app):
    desc = app["description"].lower()
    score = 0
    for word in SUSPICIOUS_KEYWORDS:
        if word in desc:
            score += 10
    return min(score, 100)

# 5) Permission suspicion
BAD_PERMISSIONS = ["READ_SMS", "READ_CONTACTS", "READ_CALL_LOG", "WRITE_SMS"]

def permission_suspicion_score(app):
    perms = app.get("permissions", [])
    score = 0
    for p in perms:
        if p in BAD_PERMISSIONS:
            score += 20
    return min(score, 100)
