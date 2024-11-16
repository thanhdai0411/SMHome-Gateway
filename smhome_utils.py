import smhome_constants

def build_topic_sensor(nodeConfig ) :
        
    sensor = nodeConfig["sensor"]
    nodeId = nodeConfig["id"]

    listSensor = list(sensor.values())
    sensor_topic = []

    for s in listSensor:
        topic = f"/{smhome_constants.ROOT_SM_HOME}/{nodeId}/{s}/value"
        sensor_topic.append(topic)
    
    return sensor_topic
    

def build_topic_button(nodeConfig) :
        
    device = nodeConfig["device"]
    nodeId = nodeConfig["id"]

    listDevice = list(device.values())
    device_topic = []

    for s in listDevice:
        topic = f"/{smhome_constants.ROOT_SM_HOME}/{nodeId}/{s}/button"
        device_topic.append(topic)
    
    return device_topic
    

