import smhome_utils

# firebase constants
DATABASE_URL = "https://sm-home-e3d95-default-rtdb.asia-southeast1.firebasedatabase.app"


MQTT_PORT = 1883
MQTT_USERNAME = 'sm-home'
MQTT_PWD = '123123'

PATH_SENSOR_KEY = "value"
PATH_DEVICE_KEY = "status"
PATH_CONFIG_KEY = "config"
PATH_BUTTON_KEY = "button"

NOTIFICATION_STATE_FILE = "notification-state.json"
NOTIFICATION_NEXT_MINUTE_TIME = 2
NODE_CONFIG_FILE = "config-node.json"

ROOT_SM_HOME = "SM_HOME"
ROOT_SM_HOME_NOTIFICATION = "SM_HOME_NOTIFICATION"

TEMP_SENSOR_ID = "SMH_SENSOR1"
HUMI_SENSOR_ID = "SMH_SENSOR2"
SR_SENSOR_ID = "SMH_SENSOR3"
GAS_SENSOR_ID = "SMH_SENSOR4"

COI_DEVICE_TOPIC_ID = "SMH_DEVICE5"

TEMP_DEVICE_ID = "01"
HUMI_DEVICE_ID = "02"
SR_DEVICE_ID = "03"
GAS_DEVICE_ID = "04"

#  Node 1
SM_HOME_NODE_1 = {
    "id" : "SMH_NODE1",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4",
        "5" : "SMH_DEVICE5",
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4",
        "5" : "SMH_SENSOR5"
    },
  
}

SM_HOME_NODE_1_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_1)
SM_HOME_NODE_1_BUTTON_TOPIC = smhome_utils.build_topic_button(SM_HOME_NODE_1)


#  Node 2
SM_HOME_NODE_2 = {
    "id" : "SMH_NODE2",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4",
        "5" : "SMH_DEVICE5",
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4"
    },
  
}

SM_HOME_NODE_2_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_2)
SM_HOME_NODE_2_BUTTON_TOPIC = smhome_utils.build_topic_button(SM_HOME_NODE_2)



#  Node 3
SM_HOME_NODE_3 = {
    "id" : "SMH_NODE3",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4",
        "5" : "SMH_DEVICE5",
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4"
    },
  
}

SM_HOME_NODE_3_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_3)
SM_HOME_NODE_3_BUTTON_TOPIC = smhome_utils.build_topic_button(SM_HOME_NODE_3)


# all
SM_HOME_ALL_SENSOR_TOPIC = SM_HOME_NODE_1_SENSOR_TOPIC + SM_HOME_NODE_2_SENSOR_TOPIC + SM_HOME_NODE_3_SENSOR_TOPIC
SM_HOME_ALL_BUTTON_TOPIC = SM_HOME_NODE_1_BUTTON_TOPIC + SM_HOME_NODE_2_BUTTON_TOPIC + SM_HOME_NODE_3_BUTTON_TOPIC


