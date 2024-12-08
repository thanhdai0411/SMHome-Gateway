from smhome_mongo import AtlasClient,ATLAS_URI,DB_NAME,COLLECTION_NAME


atlas_client = AtlasClient(ATLAS_URI, DB_NAME,COLLECTION_NAME)
atlas_client.ping()


data = atlas_client.find()
print(data)