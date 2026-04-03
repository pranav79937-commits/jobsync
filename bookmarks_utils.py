import json

FILE = "bookmarks.json"

def save_bookmark(user, job):
    try:
        data = json.load(open(FILE))
    except:
        data = {}

    data.setdefault(user, []).append(job)
    json.dump(data, open(FILE, "w"))

def load_user_bookmarks(user):
    try:
        return json.load(open(FILE)).get(user, [])
    except:
        return []
