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
    

