import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import messaging
import time
from datetime import datetime

from google.cloud.firestore_v1 import SERVER_TIMESTAMP

from smhome_mongo import AtlasClient,ATLAS_URI,DB_NAME,COLLECTION_NAME
import smhome_mqtt
import smhome_constants
import smhome_utils

# connect mongodb atlas
atlas_client = AtlasClient(ATLAS_URI, DB_NAME,COLLECTION_NAME)
atlas_client.ping()


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})


# Khởi tạo trạng thái gửi thông báo
last_send_times = smhome_utils.load_notification_state() or {}

# **********************************************************************
# firestore 
db_firestore = firestore.client()

def save_sensor_db(sensor_id, node_id, value):
    # sensor_ref = db_firestore.collection(smhome_constants.ROOT_SM_HOME).document(node_id).collection(sensor_id)
    # sensor_ref.add({
    #     "sensorId" : sensor_id,
    #     "nodeId" : node_id,
    #     'value': value,
    #     'timestamp': SERVER_TIMESTAMP  # Tự động ghi lại thời gian hiện tại
    # })


    dataInsert = {
        "sensor_id" : sensor_id,
        "node_id" : node_id,
        'value': value,
        'time': datetime.now()  # Tự động ghi lại thời gian hiện tại
    }

    atlas_client.insert_one(dataInsert)


# **********************************************************************
# connnect mqtt  
client = smhome_mqtt.connect_mqtt()
client.loop_start()


def set_realtime_db(topicSensor, dataSensor) : 
    refSensor = db.reference(topicSensor)
    refSensor.set(dataSensor)

def control_coi_alert(nodeId,sensorId, dataSensor ) : 
    if sensorId == smhome_constants.SR_SENSOR_ID or sensorId == smhome_constants.GAS_SENSOR_ID :
            configThres = smhome_utils.get_config_node(nodeId, sensorId)
            if configThres != None :
                if configThres["active"] == True : 
                    topicAlert = smhome_utils.build_topic_sensor_from_id(nodeId, smhome_constants.COI_DEVICE_TOPIC_ID)
                    smhome_mqtt.publish(client, topicAlert, dataSensor)
                    set_realtime_db(topicAlert, dataSensor)

def on_message(client, userdata, msg):
    try :
        topicSensor = msg.topic
        raw_data = msg.payload.decode("utf-8")

        sensorSplit = topicSensor.split("/")
        nodeId = sensorSplit[2]
        sensorId = sensorSplit[3]
        prefixSensor = sensorSplit[4]

        dataSensor = smhome_utils.process_frame(raw_data, sensorId)

        if not dataSensor :
            return
        
        # replace topic button to status => ref status device
        if prefixSensor == smhome_constants.PATH_BUTTON_KEY  :
            topicSensor = topicSensor.replace(prefixSensor, "status")

        # set realtime 
        print(f"topicSensor : {topicSensor}")
        set_realtime_db(topicSensor,dataSensor )

        # save firestore data sensor temp (TOPIC1) and humi (TOPIC2) only
        sensorSaveConditionTempHumi = (sensorId.split("SENSOR")[1] == "1" or sensorId.split("SENSOR")[1] == "2")
        sensorSaveConditionGasHR = (sensorId.split("SENSOR")[1] == "3" or sensorId.split("SENSOR")[1] == "4") and str(dataSensor) == "1"

        if prefixSensor ==  smhome_constants.PATH_SENSOR_KEY :
            if sensorSaveConditionTempHumi or sensorSaveConditionGasHR:
                save_sensor_db(sensorId, nodeId, dataSensor)
                

        # check coi
        control_coi_alert(nodeId,sensorId,dataSensor)
                    
        
    except Exception as e:
        print(f">>>>>>>>>>>>>>>>: {e}")



# subscrice topic  
# sensor
for topicSensor in smhome_constants.SM_HOME_ALL_SENSOR_TOPIC : 
    smhome_mqtt.subscribe(client, topicSensor, on_message)

# device
for topicDevice in smhome_constants.SM_HOME_ALL_BUTTON_TOPIC : 
    smhome_mqtt.subscribe(client, topicDevice, on_message)


# **********************************************************************
# listen firebase realtim 

ref = db.reference()

def on_message_firebase(event):
    path_all = "/"
    path_device_key = smhome_constants.PATH_DEVICE_KEY
    path_sensor = event.path.split("/")[-1] # value

    # save config node to json file
    smhome_utils.save_config_node(event, ref)

    if event.path != path_all and  path_sensor == path_device_key:

        dataPub = event.data
        
        if type(dataPub) is int or type(dataPub) is str  or type(dataPub) is bool :

            topicPub = event.path
            smhome_mqtt.publish(client, topicPub, dataPub)



my_stream = ref.listen(on_message_firebase)


