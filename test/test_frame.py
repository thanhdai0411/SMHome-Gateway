
import smhome_mqtt
import smhome_constants
from time import sleep
import base64
# connnect mqtt  
def calculate_crc16(data: str) -> str:
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return f"{crc:04X}" 

def process_frame(frame: str):
    """Phân tích và xử lý frame"""
    print(f"Frame nhận: {frame}")

    # Kiểm tra ký hiệu START và END
    if not frame.startswith("<START") or not frame.endswith("END>"):
        print("Frame không hợp lệ! Thiếu ký hiệu START hoặc END.")
        return

    # Loại bỏ START và END để xử lý dữ liệu bên trong
    #  <START,02,56.17,B3E0,END>
    content = frame[7:-5]

    parts = content.split(",")


    if len(parts) != 3:
        print("Frame không hợp lệ! Sai định dạng.")
        return

    # Phân tích các trường
    device_id, sensor_data, crc_received = parts

    # Kiểm tra CRC
    calculated_crc = calculate_crc16(f"{device_id},{sensor_data}")

    if calculated_crc != crc_received:
        print(f"CRC không khớp! CRC nhận: {crc_received}, CRC tính: {calculated_crc}")
        return

    # Xử lý dữ liệu
    print(f"Thiết bị ID: {device_id}, Dữ liệu: {sensor_data}")

def on_message(client, userdata, msg):
    """Hàm xử lý khi nhận được payload từ MQTT"""
    try :
        raw_data = msg.payload.decode("utf-8")
        process_frame(raw_data)
    except:
        print("An exception occurred")



def run():
    client = smhome_mqtt.connect_mqtt()
    
    # sensor
    for topicSensor in smhome_constants.SM_HOME_ALL_SENSOR_TOPIC : 
        smhome_mqtt.subscribe(client, topicSensor, on_message)

    # device
    for topicDevice in smhome_constants.SM_HOME_ALL_BUTTON_TOPIC : 
        smhome_mqtt.subscribe(client, topicDevice, on_message)


    client.loop_forever()
    
    
if __name__ == '__main__':
    run()
