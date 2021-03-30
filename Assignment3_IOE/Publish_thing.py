import paho.mqtt.client as paho
import os
import socket
import ssl
import random as r
import string
import json
from time import sleep
import csv
#import boto3

connflag = False
def get_random_value():
 return [r.randrange(20,35),r.randrange(85,100)]

def on_connect(client, userdata, flags, rc): # func for making connection
 global connflag
 print("Connected to AWS")
 connflag = True
 print("Connection returned result: " + str(rc))

def on_message(client, userdata, msg): # Func for Sending msg
 print(msg.topic+" "+str(msg.payload))

def connect():
 mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED,
 tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) # pass parameters

# connect to aws server
 mqttc.connect(awshost, awsport, keepalive=60)
 mqttc.loop_start()
mqttc = paho.Client() # mqttc object

# assign on_connect func
mqttc.on_connect = on_connect

# assign on_message func
mqttc.on_message = on_message

# mqttc.on_log = on_log

#### Change following parameters ####
awshost = "a1gdantso7vrsi-ats.iot.us-east-2.amazonaws.com" # Endpoint aws:iot:us-east-2:153855845931:thing/Group7Rpi
awsport = 8883 # Port no.
clientId = "Group7RPiClient-1" # Thing_Name
thingName = "Group7RPiClient" # Thing_Name

caPath = "Credentials/AmazonRootCA3.pem"                                      # Root_CA_Certificate_Name
certPath = "Credentials/33c6aeda67-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "Credentials/33c6aeda67-private.pem.key"                          # <Thing_Name>.private.key

i = 0
connect()
while i<=20:
    sleep(5)
    json_data = dict()
    data = dict()
    temp, hum = get_random_value()
    data["temperature"] = temp
    data["humidity"] = hum
    json_data[clientId] = data
    payload_json = json.dumps(json_data)
    # topic: temperature # Publishing Temperature values
    mqttc.publish("Group7Rpi", payload_json, qos=1)
    print(json_data)
    i+=1
