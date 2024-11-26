import json

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
    

def build_ref_config_sensor_node(nodeId , sensorId ) :
    return f"{smhome_constants.ROOT_SM_HOME}/{nodeId}/{sensorId}/config"
    

def save_config_node(event, ref):
    path_all = "/"
    path_config_key = smhome_constants.PATH_CONFIG_KEY
    path_config = event.path.split("/")[-1] # config

    path = event.path

    if path == path_all or path_config == path_config_key :
        refetchData = ref.get(smhome_constants.ROOT_SM_HOME)   
        objectData =  refetchData[0]
        json_object = json.dumps(objectData, indent=4)
        with open(smhome_constants.NODE_CONFIG_FILE, "w") as outfile:
            outfile.write(json_object)

def get_config_node(nodeId , sensorId) : 
    if os.path.exists(smhome_constants.NODE_CONFIG_FILE):
        with open(smhome_constants.NODE_CONFIG_FILE, 'r') as openfile:
            json_object = json.load(openfile)
    
        direction = smhome_constants.ROOT_SM_HOME
        getConfigSensor = json_object[smhome_constants.ROOT_SM_HOME][nodeId][sensorId][smhome_constants.PATH_CONFIG_KEY]
        return {
            "minThreshold" : getConfigSensor["minThreshold"],
            "maxThreshold" : getConfigSensor["maxThreshold"],
            "name" : getConfigSensor["name"]
        }
    return {}  


def load_notification_state():
    if os.path.exists(smhome_constants.NOTIFICATION_STATE_FILE):
        with open(smhome_constants.NOTIFICATION_STATE_FILE, "r") as file:
            return json.load(file)
    return None  

def save_notification_state(state):
    with open(smhome_constants.NOTIFICATION_STATE_FILE, "w") as file:
        json.dump(state, file)


def can_send_notification(sensorId, last_send_times):
    
    current_time = time.time()  
    last_time = float(last_send_times.get(sensorId, 0))  

    if current_time - last_time >= smhome_constants.NOTIFICATION_NEXT_MINUTE_TIME: 
        last_send_times[sensorId] = current_time  
        save_notification_state(last_send_times) 
        return True
    return False
