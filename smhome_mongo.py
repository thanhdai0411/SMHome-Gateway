from pymongo import MongoClient

ATLAS_URI = "mongodb+srv://smhome:i24aOz4mJTNRN7aV@cluster0.bfhjy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = 'sm_home'
COLLECTION_NAME = 'sensor'


class AtlasClient ():
    def __init__ (self, altas_uri, dbname, collection_name ):
        self.mongodb_client = MongoClient(altas_uri)
        self.database = self.mongodb_client[dbname]
        self.collection = self.mongodb_client[dbname][collection_name]

    def ping (self):
        self.mongodb_client.sm_home.command('ping')
        print ('Connected to MongoDB Atlas success !!!')


    def get_collection (self):
        collection = self.collection
        return collection

    def find (self, filter = {}, limit=0):
        collection = self.collection
        items = list(collection.find(filter=filter, limit=limit))
        return items

    def insert_one(self, data) :
        collection = self.collection
        return collection.insert_one(data)

    def insert_many(self, datas) :
        collection = self.collection
        return collection.insert_many(datas)
    
    def update_one(self, myquery, newvalues) :
        collection = self.collection
        return collection.update_one(myquery, newvalues)

    def delete_one(self, myquery) :
        collection = self.collection
        return collection.delete_one(myquery)
    
    


