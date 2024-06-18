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
    # get all collections (sensor devices with 'COM' prefix)
    collections = db.list_collection_names()
    sensor_data = {}
    for collection in collections:
        if collection.startswith("COM"):
            cursor = db[collection].find({}, {'_id': 0}).sort('Datetime', -1).limit(1)
            sensor_data[collection] = cursor
    sensor_device_data = {}
    """
        device_data = {
            'COM1': cursor1,
            'COM2': cursor2,
            ...
        }
        """
    for device in sensor_data:
        sensor_data[device] = sensor_data[device].next()  # get the first element of the cursor

    return sensor_data


def get_latest_edge_data(farm_id):
    client = pymongo.MongoClient(mongo_uri)
    db = client[str(farm_id)]
    # get collection name EdgeHealth
    collection = db["EdgeHealth"]
    cursor = collection.find({}, {'_id': 0}).sort('Datetime', -1).limit(1)
    edge_data = cursor.next()

    # reformat data to be matched with the sensor data
    camera_state = edge_data.pop('CameraState')
    edge_device_data = {}
    for camera_edge in camera_state:
        # only get IPO and LastResponse
        edge_device_data[camera_edge.get('Name')] = {'IP': camera_edge.get('IP'),
                                                     'LastResponse': camera_edge.get('LastResponse')}

    return edge_device_data
    # edge_data -> get name: Edge_1 -> [key]:  IP | LastResponse


if __name__ == "__main__":
    data = get_all_users()
    for d in data:
        print(d)
