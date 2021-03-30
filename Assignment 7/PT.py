import paho.mqtt.client as paho
import os
import socket
import ssl
import random as r
import string
import json
from time import sleep
import csv
connflag = False


def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))
    client.subscribe("Topic2")


def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))


def connect():
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
                  tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
# connect to aws server
    mqttc.connect(awshost, awsport, keepalive=60)

    mqttc.loop_start()


mqttc = paho.Client()
# mqttc-subscribe = paho.Client()# mqttc object
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message func
mqttc.on_message = on_message
# mqttc.on_log = on_log

#### Change following parameters ####
awshost = "a2uhbgx7lzzjrs-ats.iot.ap-south-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.
clientId = "Group4RaspberyPiClient"                                     # Thing_Name
thingName = "Group4RaspberyPiClient"                                    # Thing_Name
# Root_CA_Certificate_Name

caPath = "../Creds/{}".format("AmazonRootCA1_2.pem")
# <Thing_Name>.cert.pem
certPath = "../Creds/{}".format("16012f240a-certificate.pem.crt")
# <Thing_Name>.private.key
keyPath = "../Creds/{}".format("16012f240a-private.pem.key")i=0
connect()
while i <= 20:
    
    if connflag == True:
        json_data = dict()
        temp = round(r.uniform(25, 35), ndigits=2)
        hum = round(r.uniform(85, 100), ndigits=2)
        json_data["temperature"] = temp
        json_data["humidity"] = hum
        json_data["client_name"] = clientId
        payload_json = json.dumps(json_data)
        # topic: temperature # Publishing Temperature values
        mqttc.publish("Topic1", payload_json, qos=1)
        # dyanmodb = boto3.resource("dynamodb", endpoint_url="")
        print("msg sent: Group4")  # Print sent temperature msg on console
        print(payload_json)
    else:
        print("waiting for connection...")
    i += 1
    sleep(15)
