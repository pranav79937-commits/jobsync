import json
from datetime import datetime

FILE = "applications.json"

def track_application(user, job):
    try:
        data = json.load(open(FILE))
    except:
        data = {}

    data.setdefault(user, []).append({
        **job,
        "applied_on": datetime.now().strftime("%Y-%m-%d")
    })

    json.dump(data, open(FILE, "w"))

def get_user_applications(user):
    try:
        return json.load(open(FILE)).get(user, [])
    except:
        return []
