import smhome_utils

# firebase constants
DATABASE_URL = "https://sm-home-e3d95-default-rtdb.asia-southeast1.firebasedatabase.app"

# mqtt 

MQTT_PORT = 1883
MQTT_USERNAME = 'sm-home'
MQTT_PWD = '123123'

# device id config
ROOT_SM_HOME = "SM_HOME"

#  Node 1
SM_HOME_NODE_1 = {
    "id" : "SMH_NODE1",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4"
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4"
    },
  
}

SM_HOME_NODE_1_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_1)


#  Node 2
SM_HOME_NODE_2 = {
    "id" : "SMH_NODE2",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4"
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4"
    },
  
}

SM_HOME_NODE_2_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_2)


#  Node 3
SM_HOME_NODE_3 = {
    "id" : "SMH_NODE3",
    "device": {
        "1" : "SMH_DEVICE1",
        "2" : "SMH_DEVICE2",
        "3" : "SMH_DEVICE3",
        "4" : "SMH_DEVICE4"
    },
    "sensor": {
        "1" : "SMH_SENSOR1",
        "2" : "SMH_SENSOR2",
        "3" : "SMH_SENSOR3",
        "4" : "SMH_SENSOR4"
    },
  
}

SM_HOME_NODE_3_SENSOR_TOPIC = smhome_utils.build_topic_sensor(SM_HOME_NODE_3)



SM_HOME_ALL_SENSOR_TOPIC = SM_HOME_NODE_1_SENSOR_TOPIC + SM_HOME_NODE_2_SENSOR_TOPIC + SM_HOME_NODE_3_SENSOR_TOPIC