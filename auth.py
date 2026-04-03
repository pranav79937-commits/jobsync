import json, hashlib

FILE = "users.json"

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def signup(u, p):
    try:
        users = json.load(open(FILE))
    except:
        users = []

    for user in users:
        if user["username"] == u:
            return False, "User exists"

    users.append({"username": u, "password": hash_password(p)})
    json.dump(users, open(FILE, "w"))
    return True, "Created"

def login(u, p):
    try:
        users = json.load(open(FILE))
    except:
        return False

    for user in users:
        if user["username"] == u and user["password"] == hash_password(p):
            return True
    return False
