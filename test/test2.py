import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import messaging
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
import time
import json

import smhome_constants
import smhome_utils


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})

db_firestore = firestore.client()
ref = db.reference()

def on_message_firebase(event):
    smhome_utils.save_config_node(event, ref)


def get_test():
    res = smhome_utils.get_config_node("SMH_NODE1", "SMH_SENSOR1")
    print(res)


get_test()

# my_stream = ref.listen(on_message_firebase)