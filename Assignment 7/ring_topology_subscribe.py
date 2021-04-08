# Import package
import paho.mqtt.client as mqtt
import ssl
import json

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
# MQTT_TOPIC = "helloTopic"
# MQTT_TOPIC = "IOE7-Central-Device-Subscribe"
MQTT_TOPIC_SUBSCRIBE = "Group-15-A"
MQTT_TOPIC_PUBLISH = "Group-11-B"
MQTT_MSG = "hello MQTT"

# **** Ring Topology Path ****
ring_path = {
    "Group-15-A" : "Group-11-B",
    "Group-11-B" : "Group-13-A",
    "Group-13-B" : "Group-15-B",
    "Group-15-B" : "Group-14-A",
    "Group-14-A" : "Group-11-A",
    "Group-11-A" : "Group-13-B",
    "Group-13-B" : "Group-14-B",
    "Group-14-B" : "Group-15-A",
}

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



# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, rc,  properties=None):
    mqttc.subscribe(MQTT_TOPIC_SUBSCRIBE, 0)


def on_publish(client, userdata, mid):
	print("Message Published...")


# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
    print("Topic: " + str(msg.topic))
    print("QoS: " + str(msg.qos))
    print("Payload: " + str(msg.payload))

    payload = json.loads(msg.payload.decode())
    if payload["headers"]["destination"] == MQTT_TOPIC_SUBSCRIBE:
        print("Data Receieved : \n", payload)
    else :
        print("Data received... \n Destination : ", payload["headers"]["destination"], " Source : ", payload["headers"]["source"])
        if "intermediate_node" in payload :
            print("Received from ", payload["intermediate_node"][-1])
            payload["intermediate_node"].append(MQTT_TOPIC_SUBSCRIBE)
        else :
            payload.setdefault("intermediate_node", [MQTT_TOPIC_SUBSCRIBE])
        print("Forwarding to ", MQTT_TOPIC_PUBLISH)

        mqttc.publish(MQTT_TOPIC_PUBLISH, json.dumps(payload),qos=1)

    # mqttc.publish('IOE7-Central-Device-Subscribe',msg.payload.decode(),qos=1)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + 
	MQTT_MSG + " with QoS: " + str(granted_qos))
    # mqttc.publish('IOE7-Central-Device-Subscribe',"testing",qos=1)

# Initiate MQTT Client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()