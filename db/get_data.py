# read User's information from Mongo database
def get_all_users():
    import pymongo

    mongo_uri = "mongodb://localhost:27017/"
    client = pymongo.MongoClient(mongo_uri)
    db = client["FarmManagement"]
    collection = db["Users"]
