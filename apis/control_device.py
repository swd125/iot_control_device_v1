import json
import time
from paho.mqtt import client as mqtt_client
import ssl

broker = 'a31dvipl38h049-ats.iot.ap-southeast-1.amazonaws.com'
port = 8883
topic = "control/807D3AC722E8"

def connect_mqtt():

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    client = mqtt_client.Client("mqtt-ball-1")
    client.tls_set(
        ca_certs = '/home/swd125/Desktop/Cert/mqtt_aws/cert/AmazonRootCA1.pem',
        certfile = '/home/swd125/Desktop/Cert/mqtt_aws/cert/iot-core-certificate.pem.crt',
        keyfile  = '/home/swd125/Desktop/Cert/mqtt_aws/cert/iot-core-private.pem.key',
        tls_version = ssl.PROTOCOL_TLSv1_2
    )
    client.on_connect = on_connect
    client.connect(broker, port)
    # print(f'{client = }')
    return client


def publish(client, toggle):
    msg = {
            "control_led": toggle
        }

    result = client.publish(topic, json.dumps(msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def control_device():
    client = connect_mqtt()
    client.loop_start()
    toggle = 1
    for i in range(10):
        time.sleep(2)
        publish(client, toggle)
        toggle = 0 if toggle else 1
    client.loop_stop()
    return 'complete'


if __name__ == '__main__':
    control_device()