import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import smhome_mqtt
import smhome_constants

# firebase constant


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})


ref = db.reference()
# ref.set(data)


# connnect mqtt 
client = smhome_mqtt.connect_mqtt()
client.loop_start()


def on_message(client, userdata, msg):
    print(f"[SUB]:   Received `{msg.payload.decode()}` from `{msg.topic}` topic")


for topicSensor in smhome_constants.SM_HOME_ALL_SENSOR_TOPIC : 
    smhome_mqtt.subscribe(client, topicSensor, on_message)


# listen firebase realtim
def on_message(event):
    path_all = "/"
    if event.path != path_all:
        print("---------------------------------------------------------------")
        print('[{}] :: {}'.format(event.path, event.data))

        dataPub = event.data
        
        if type(dataPub) is int or type(dataPub) is str  or type(dataPub) is bool :

            topicPub = event.path
            smhome_mqtt.publish(client, topicPub, dataPub)


    
my_stream = ref.listen(on_message)


