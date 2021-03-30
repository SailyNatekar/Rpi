# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random as r
import string
import json
import datetime as dt
from time import sleep
from random import uniform
from generate import DataGenerator as d

 
connflag = False

def connect():
 mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None) # pass parameters


def get_random_value():
 return [r.randrange(20,35),r.randrange(85,100)]

def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print ("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
     print(msg.topic+" "+str(msg.payload))
    

 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a1gdantso7vrsi-ats.iot.us-east-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "Group7Rpi_thing1_Saily"                                     # Thing_Name
thingName = "Rpi"                                    # Thing_Name
caPath = "Assignment 7/Certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "Assignment 7/Certificates/Thing2 cred/33c6aeda67-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "Assignment 7/Certificates/Thing2 cred/33c6aeda67-private.pem.key"                          # <Thing_Name>.private.key
 
#mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop

i = 0
connect()
while i<=20:
    sleep(5)
   
    json_data = dict()
    data = dict()
    temp,moisture = get_random_value()
    data["temperature"] = temp
    data["moisture"] = moisture
    json_data[clientId] = data
    payload_json = json.dumps(json_data)

       # temp,moisture = d().get_random_value() 
       # dictionary = {""temp":temp,"moisture":moisture, "timestamp":str(dt.datetime.now())}
       # paylodmsg_json = json.dumps(dictionary)       
    mqttc.publish("Moisture", payload_json , qos=1)        # topic: temperature # Publishing Temperature values
    print("msg sent: Soil Monitoring" ) # Print sent temperature msg on console
    print(json_data)
    i+=1

 #   else:
  #      print("waiting for connection...")                      