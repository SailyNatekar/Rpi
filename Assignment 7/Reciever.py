import paho.mqtt.client as paho
import os
import socket
import ssl
import ast
import datetime as dt


def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # Subscribe to all topics
    client.subscribe("Group8", 1)


def on_message(client, userdata, msg):
    # Func for receiving msgs
    print("topic: "+msg.topic)
    print("Received by: Group 7")
    print("payload: "+str(msg.payload))



mqttc = paho.Client()                                       # mqttc object
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message func
mqttc.on_message = on_message
#mqttc.on_log = on_log

#### Change following parameters ####
awshost = "a1gdantso7vrsi-ats.iot.us-east-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.
clientId = "Thing4"                                     # Thing_Name
thingName = "Thing4"                                    # Thing_Name
# Root_CA_Certificate_Name

caPath = "Certificates/AmazonRootCA1.pem"

# <Thing_Name>.cert.pem
certPath = "Certificates/Thing3 cred/ad03d2c46e-certificate.pem.crt"
# <Thing_Name>.private.key
keyPath = "Certificates/Thing3 cred/ad03d2c46e-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# connect to aws server
mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()

