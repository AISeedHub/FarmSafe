import pymongo
import yaml

# read the configuration file
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
    mongo_uri = config['mongo_uri']


# read User's information from Mongo database
def get_all_users():
    client = pymongo.MongoClient(mongo_uri)
    db = client["FarmManagement"]
    collection = db["User"]
    data = collection.find()
    return data


def get_admin_email():  # not tested
    client = pymongo.MongoClient(mongo_uri)
    db = client["FarmManagement"]
    collection = db["User"]
    data = collection.find_one({"role": "admin"})
    return data['email']


# get all Farms information from Mongo database
def get_all_farms():
    client = pymongo.MongoClient(mongo_uri)
    db = client["FarmManagement"]
    collection = db["Farms"]
    data = collection.find()
    return data


def get_latest_sensor_data(farm_id):
    client = pymongo.MongoClient(mongo_uri)
    db = client[str(farm_id)]
    # get all collections (sensor devices)
    collections = db.list_collection_names()
    # for each collection, get the latest data
    sensor_data = {
        collection: db[collection].find({}, {'_id': 0}).sort('Datetime', -1).limit(1)
        for collection in collections
    }
    return sensor_data


if __name__ == "__main__":
    data = get_all_users()
    for d in data:
        print(d)
