import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from google.cloud.firestore_v1 import SERVER_TIMESTAMP

import smhome_mqtt
import smhome_constants
import smhome_utils


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})


# Khởi tạo trạng thái gửi thông báo
last_send_times = smhome_utils.load_notification_state()

# **********************************************************************
# firestore 
db_firestore = firestore.client()

def save_sensor_firestore(sensor_id, node_id, value):
    sensor_ref = db_firestore.collection(smhome_constants.ROOT_SM_HOME).document(node_id).collection(sensor_id)
    sensor_ref.add({
        "sensorId" : sensor_id,
        "nodeId" : node_id,
        'value': value,
        'timestamp': SERVER_TIMESTAMP  # Tự động ghi lại thời gian hiện tại
    })

    print(f'[FireStore]:   Sensor data save ::: {sensor_id}')

# **********************************************************************
# sent notification 
def get_all_tokens():
    try:
        tokens_ref = db_firestore.collection_group(smhome_constants.ROOT_SM_HOME_NOTIFICATION)
        tokens = tokens_ref.stream()

        tokenUsers = []
        for token in tokens:
            token_data = token.to_dict()
            token_id = token.id
            tokenUsers.append({
                "token" : token_data['token'] , 
                "id" : token.id
            })

        seen_tokens = set()  # Tập hợp để theo dõi các token đã gặp
        unique_list = []     # Danh sách kết quả

        for item in tokenUsers:
            if item["token"] not in seen_tokens:
                seen_tokens.add(item["token"])
                unique_list.append(item)

        return unique_list
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        return []


def send_message_to_tokens(title, body):
    tokens = get_all_tokens()
    for objectToken in tokens:
        attempts = 0  # Đếm số lần thử gửi
        success = False
        
        token = objectToken["token"] 
        idToken = objectToken["id"]

        while attempts < 3 and not success:
            try:
                # Cấu hình nội dung thông báo
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body,
                    ),
                    token=token,  # Gửi từng token
                )

                # Gửi thông báo
                response = messaging.send(message)
                print(f"Thông báo gửi thành công đến token: {token}")
                print(f"Response: {response}")
                
                success = True  # Gửi thành công, thoát khỏi vòng lặp
                
            except Exception as e:
                attempts += 1
                print(f"Lỗi khi gửi thông báo tới token {token}, lần thử {attempts}: {e}")
                if attempts < 3:
                    time.sleep(5)  # Retry sau 5 giây

        if not success:

            # delete document
            doc_ref = db.collection(smhome_constants.ROOT_SM_HOME_NOTIFICATION).document(idToken)
            doc_ref.delete()

            print(f"Delete token {token} sau 3 lần thử không thành công.")

    print("Hoàn thành việc gửi thông báo.")


def action_send_notify(cofigThres, dataSensor, sensorId) :
    minT = cofigThres["minThreshold"]
    maxT = cofigThres["maxThreshold"]
    nameSensor = cofigThres["name"]

    conditionSentMinThresh = minT and (int(dataSensor) < int(minT))
    conditionSentMaxThresh = maxT and (int(dataSensor) > int(maxT))


    conditionDetect = int(dataSensor) == 1


    titleMsg = "Cảnh báo vượt ngưỡng"
    minBody = nameSensor + " có giá trị " + dataSensor + " vượt ngưỡng Min"
    maxBody = nameSensor + " có giá trị " + dataSensor + " vượt ngưỡng Max"

    titleSR = "Cảnh báo"
    bodySR = "Có người đột nhập"

    titleGAS = "Cảnh báo"
    bodyGAS = "Phát hiện rò rỉ khí gas hoặc có khói"


    # temp and humi
    if sensorId in [smhome_constants.TEMP_SENSOR_ID, smhome_constants.HUMI_SENSOR_ID] : 
        if conditionSentMinThresh and smhome_utils.can_send_notification(sensorId, last_send_times) :
            send_message_to_tokens(titleMsg, minBody)
        
        if conditionSentMaxThresh and smhome_utils.can_send_notification(sensorId, last_send_times):
            send_message_to_tokens(titleMsg, maxBody)

    # sr : chuyen dong
    elif  smhome_constants.SR_SENSOR_ID  : 
        if conditionDetect and smhome_utils.can_send_notification(sensorId, last_send_times) :
            send_message_to_tokens(titleSR, bodySR)

    # gas   
    elif  smhome_constants.GAS_SENSOR_ID  : 
        if conditionDetect and smhome_utils.can_send_notification(sensorId, last_send_times) :
            send_message_to_tokens(titleGAS, bodyGAS)
       

# **********************************************************************
# connnect mqtt  
client = smhome_mqtt.connect_mqtt()
client.loop_start()


def on_message(client, userdata, msg):
                                                                                                                                                                                                                                  
    topicSensor = msg.topic

    # split frame send
    dataSensor = msg.payload.decode()

    # spilit add firestore
    sensorSplit = topicSensor.split("/")
    nodeId = sensorSplit[2]
    sensorId = sensorSplit[3]
    prefixSensor = sensorSplit[4]

    # replace topic button to status => ref status device
    if(prefixSensor == smhome_constants.PATH_BUTTON_KEY ) :
        topicSensor = topicSensor.replace(prefixSensor, "status")

    # set realtime 
    refSensor = db.reference(topicSensor)
    refSensor.set(dataSensor)

    # save firestore data sensor temp (TOPIC1) and humi (TOPIC2) only
    if prefixSensor ==  smhome_constants.PATH_SENSOR_KEY and (sensorId.split("SENSOR")[1] == "1" or sensorId.split("SENSOR")[1] == "2") :
        print("save sensor")
        save_sensor_firestore(sensorId, nodeId, dataSensor)

       
    cofigThres = smhome_utils.get_config_node(nodeId, sensorId)
    if cofigThres != None : 
        action_send_notify(cofigThres, dataSensor, sensorId )
       



    
    # log
    print(f"[SUB]:   Received `{dataSensor}` from `{topicSensor}` topic")


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
        print("---------------------------------------------------------------")
        print('[{}] :: {}'.format(event.path, event.data))

        dataPub = event.data
        
        if type(dataPub) is int or type(dataPub) is str  or type(dataPub) is bool :

            topicPub = event.path
            smhome_mqtt.publish(client, topicPub, dataPub)



my_stream = ref.listen(on_message_firebase)


