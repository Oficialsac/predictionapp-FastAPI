import json 

db_path = 'auth/fakedb.json'

def read_file():
    with open(db_path) as db_file:
        db = json.load(db_file)
    return db

def write_file(data: dict):
    with open(db_path, 'w') as db_file:
        json.dump(data, db_file)
    
    return True