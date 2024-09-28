import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

import smhome_mqtt
import smhome_constants


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})

# firebase realtime
ref = db.reference()

# firestore
db_firestore = firestore.client()

print(db_firestore)


def save_sensor_firestore(sensor_id, node_id, value):
    sensor_ref = db_firestore.collection(smhome_constants.ROOT_SM_HOME).document(node_id).collection(sensor_id)
    sensor_ref.add({
        "sensorId" : sensor_id,
        "nodeId" : node_id,
        'value': value,
        'timestamp': SERVER_TIMESTAMP  # Tự động ghi lại thời gian hiện tại
    })

    print(f'[FireStore]:   Sensor data save ::: {sensor_id}')


# connnect mqtt 
client = smhome_mqtt.connect_mqtt()
client.loop_start()


def on_message(client, userdata, msg):

    topicSensor = msg.topic
    dataSensor = msg.payload.decode()

    # set realtime
    refSensor = db.reference(topicSensor)
    refSensor.set(dataSensor)

    # spilit add firestore
    sensorSplit = topicSensor.split("/")
    nodeId = sensorSplit[2]
    sensorId = sensorSplit[3]
    save_sensor_firestore(sensorId, nodeId, dataSensor )


    # log
    print(f"[SUB]:   Received `{dataSensor}` from `{topicSensor}` topic")


for topicSensor in smhome_constants.SM_HOME_ALL_SENSOR_TOPIC : 
    smhome_mqtt.subscribe(client, topicSensor, on_message)


# listen firebase realtim
def on_message_firebase(event):
    path_all = "/"
    path_sensor_key = "value"
    path_sensor = event.path.split("/")[-1] # value

    

    if event.path != path_all and  path_sensor != path_sensor_key:
        print("---------------------------------------------------------------")
        print('[{}] :: {}'.format(event.path, event.data))

        dataPub = event.data
        
        if type(dataPub) is int or type(dataPub) is str  or type(dataPub) is bool :

            topicPub = event.path
            smhome_mqtt.publish(client, topicPub, dataPub)


    
my_stream = ref.listen(on_message_firebase)


