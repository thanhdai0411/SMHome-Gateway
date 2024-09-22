import socket

import random
import time

from paho.mqtt import client as mqtt_client
import smhome_constants

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

print('>>> MQTT BROKER: {}'.format(s.getsockname()[0]))


broker = s.getsockname()[0]
port = smhome_constants.MQTT_PORT
username = smhome_constants.MQTT_USERNAME
password = smhome_constants.MQTT_PWD

s.close()


def on_connect(client, userdata, flags, rc, properties):    
    if rc == 0:
        print("Connected to MQTT Broker !")
    else:
        print("Failed to connect, return code %d\n", rc)


def subscribe(client: mqtt_client, topic, on_message):
    client.subscribe(topic)
    client.on_message = on_message


def publish(client, topic,  msg):
    
    result = client.publish(topic, msg)
    # result: [0, 1]

    status = result[0]
    if status == 0:
        print(f"[PUB]:   Success pub `{msg}` to topic `{topic}`")
    else:
        print(f"[PUB]:   Failed to pub message to topic {topic}")
       


def connect_mqtt():
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)

    client.on_connect = on_connect
    
    client.connect(broker, port)
    return client


# def run():
#     client = connect_mqtt()
#     client.loop_start()

#     subscribe(client, "hello")
#     publish(client, "hello", "hello ae nhe")

#     client.loop_forever()
    
    
# if __name__ == '__main__':
#     run()
