import json
import os
import smhome_constants 
import time 

def build_topic_sensor(nodeConfig ) :
        
    sensor = nodeConfig["sensor"]
    nodeId = nodeConfig["id"]

    listSensor = list(sensor.values())
    sensor_topic = []

    for s in listSensor:
        topic = f"/{smhome_constants.ROOT_SM_HOME}/{nodeId}/{s}/value"
        sensor_topic.append(topic)
    
    return sensor_topic


def build_topic_sensor_from_id(nodeId, id) :
    return f"/{smhome_constants.ROOT_SM_HOME}/{nodeId}/{id}/status"

def build_topic_start_node(nodeId) :
    return f"/{smhome_constants.ROOT_SM_HOME}/{nodeId}/start"

def check_topic_start_node(nodeId, topic) :
    topicReal = build_topic_start_node(nodeId)
    return topicReal == topic


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
            "name" : getConfigSensor["name"],
            "active" : getConfigSensor["active"],
            "isAlert" : getConfigSensor["isAlert"]
        }
    return None


def get_prev_data_node(nodeId) : 
    if os.path.exists(smhome_constants.NODE_CONFIG_FILE):
        with open(smhome_constants.NODE_CONFIG_FILE, 'r') as openfile:
            json_object = json.load(openfile)
    
        direction = smhome_constants.ROOT_SM_HOME
        getConfigSensor = json_object[smhome_constants.ROOT_SM_HOME][nodeId]
        return getConfigSensor
    return None


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
    print(f"last_send_times: {last_send_times}")
    if not last_send_times : 
        last_send_times[sensorId] = current_time  
        save_notification_state(last_send_times) 
        return True

    last_time = float(last_send_times.get(sensorId, 0))  

    print(f"last_time: {last_time}")

    if current_time - last_time >= smhome_constants.NOTIFICATION_NEXT_MINUTE_TIME: 
        last_send_times[sensorId] = current_time  
        save_notification_state(last_send_times) 
        return True
    return False
   
    



# build frame

def calculate_crc16(data: str) -> str:
    """Tính CRC-16"""
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return f"{crc:04X}"  # Trả về CRC dưới dạng chuỗi hex 4 ký tự

def checkDeviceId(deviceId : str) :
    check = {
        smhome_constants.TEMP_DEVICE_ID : smhome_constants.TEMP_SENSOR_ID,
        smhome_constants.HUMI_DEVICE_ID : smhome_constants.HUMI_SENSOR_ID,
        smhome_constants.SR_DEVICE_ID : smhome_constants.SR_SENSOR_ID,
        smhome_constants.GAS_DEVICE_ID : smhome_constants.GAS_SENSOR_ID,   
        smhome_constants.KHOI_DEVICE_ID : smhome_constants.KHOI_SENSOR_ID,   
        smhome_constants.RELAY1_DEVICE_ID : smhome_constants.RELAY1_TOPIC_ID,
        smhome_constants.RELAY2_DEVICE_ID : smhome_constants.RELAY2_TOPIC_ID,
        smhome_constants.RELAY3_DEVICE_ID : smhome_constants.RELAY3_TOPIC_ID,
        smhome_constants.RELAY4_DEVICE_ID : smhome_constants.RELAY4_TOPIC_ID,
        smhome_constants.RELAY5_DEVICE_ID : smhome_constants.RELAY5_TOPIC_ID,

    }

        
    try:
        return check[deviceId]
    except:
        return None



def process_frame(frame: str):
    """Phân tích và xử lý frame"""
    
    # <START,02,56.17,B3E0,END>
    
    # Kiểm tra ký hiệu START và END
    if not frame.startswith("<START") or not frame.endswith("END>"):
        print("Frame không hợp lệ! Thiếu ký hiệu START hoặc END.")
        return


    content = frame[7:-5]
    # 02, 56.17 , B3E0

    parts = content.split(",")

    # [02 ; 56.17 ; B3E0]

    if len(parts) != 3:
        print("Frame không hợp lệ! Sai định dạng.")
        return

    # Phân tích các trường
    device_id, sensor_data, crc_received = parts
    

    # check device id with topic 
    if not checkDeviceId(device_id):
        print("Device Id invalid")
        return 

    # Kiểm tra CRC
    calculated_crc = calculate_crc16(f"{device_id},{sensor_data}")

    if calculated_crc != crc_received:
        print(f"CRC không khớp! CRC nhận: {crc_received}, CRC tính: {calculated_crc}")
        return


    return sensor_data
