# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
from time import sleep
from random import uniform
import datetime
import csv
 
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
    
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a1gdantso7vrsi-ats.iot.us-east-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "sensor1"                                     # Thing_Name
thingName = "sensor1"                                    # Thing_Name
caPath = "Certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "Certificates/Thing2 cred/33c6aeda67-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "Certificates/Thing2 cred/33c6aeda67-private.pem.key"                          # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
while 1==1:
    sleep(1)
    if connflag == True:
        data = dict()
        json_data = dict()
        height = uniform(20.0, 35.0)
        pressure = uniform(70, 85)
        data["time"] = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
        data["height"] = height
        data["pressure"] = pressure
        data["path"] = ["Saily-1"]
        json_data["Saily-1"] = data
        paylodmsg = json.dumps(json_data) 
        mqttc.publish("Ring1", paylodmsg , qos=1)        # topic: topic # Publishing Temperature values
        print("msg sent: Ring1" ) # Print sent temperature msg on console
        print(paylodmsg)
    else:
        print("waiting for connection...")