# Import package
import paho.mqtt.client as mqtt
import ssl
import time
import random as r
import json

def get_random_value():
    return [r.randrange(20,35),r.randrange(85,100)]


# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "Group-11-B"
MQTT_MSG = "hello From Harshita "

# Group-15 Credentials
# MQTT_HOST = "a3dcijkkcxyx7s-ats.iot.us-east-1.amazonaws.com"
# CA_ROOT_CERT_FILE = "Amazon_Root_CA_1.pem"
# THING_CERT_FILE = "0b3e28ad67-certificate.pem.crt"
# THING_PRIVATE_KEY = "0b3e28ad67-private.pem.key"

# GROUP-14 Credentials
MQTT_HOST = "a2y1m4l5nyoj4c-ats.iot.us-east-2.amazonaws.com"
CA_ROOT_CERT_FILE = "./Group-14/AmazonRootCA1.pem"
THING_CERT_FILE = "./Group-14/95571a36ac-certificate.pem.crt"
THING_PRIVATE_KEY = "./Group-14/95571a36ac-private.pem.key"

# GROUP-13 Credentials
# MQTT_HOST = "a2fxqdjjnurfko-ats.iot.us-east-2.amazonaws.com"
# CA_ROOT_CERT_FILE = "./Group-13/AmazonRootCA1.pem"
# THING_CERT_FILE = "./Group-13/427d3049ad-certificate.pem.crt"
# THING_PRIVATE_KEY = "./Group-13/427d3049ad-private.pem.key"

# GROUP-11 Credentials
# MQTT_HOST = "a25gshlawby7lu-ats.iot.ap-south-1.amazonaws.com"
# CA_ROOT_CERT_FILE = "./Group-11/AmazonRootCA1.pem"
# THING_CERT_FILE = "./Group-11/65f3d674c0-certificate.pem.crt"
# THING_PRIVATE_KEY = "./Group-11/65f3d674c0-private.pem.key"




# Define on_publish event function
def on_publish(client, userdata, mid):
	print("Message Published...")


# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)		
mqttc.loop_start()

counter = 0
while True:
    values = get_random_value() 
    MQTT_MSG = json.dumps({"data" : {"temperature" : values[0], "humidity" : values[1]}, "headers": {"source" : "Group-15-A", "destination" : "Group-13-A"}})

    mqttc.publish(MQTT_TOPIC,MQTT_MSG,qos=1)
    # counter += 1
    time.sleep(25)

# Disconnect from MQTT_Broker
# mqttc.disconnect()