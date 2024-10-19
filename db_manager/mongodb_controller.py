from pymongo import MongoClient

def get_mongo_client():
    client = MongoClient('localhost', 27017)
    return client

def get_mongo_database(db_name):
    client = get_mongo_client()
    db = client[db_name]
    return db