# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import pandas as pd
import ast
import datetime as dt


def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # Subscribe to all topics
    client.subscribe("Moisture", 1)


data = list()
i = 0


def on_message(client, userdata, msg):
    # Func for receiving msgs
    global data
    global i
    if flag == 1:
        print("topic: "+msg.topic)
        print("payload: "+str(msg.payload))
    elif flag == 2:
        byte_str = msg.payload
        dict_str = byte_str.decode("utf-8")
        d = ast.literal_eval(dict_str)
        data.append(d)
        if len(data) == 10:
            fp = open("collectedData.csv", "w", encoding="utf-8")
            df = pd.DataFrame(data)
            df.to_csv(fp)
            print("File generated")
        i += 1


flag = int(input("Select what to do with the data recieved\n1. Display the data\n2. Store it in a file\n Select your choice: "))
 
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

#### Change following parameters #### 
awshost = "a1gdantso7vrsi-ats.iot.us-east-2.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "Group7Rpi_thing1"                                     # Thing_Name
thingName = "Rpi"                                    # Thing_Name
caPath = "Assignment 7/Certificates/AmazonRootCA1.pem"                                      # Root_CA_Certificate_Name
certPath = "Assignment 7/Certificates/Thing2 cred/33c6aeda67-certificate.pem.crt"                            # <Thing_Name>.cert.pem
keyPath = "Assignment 7/Certificates/Thing2 cred/33c6aeda67-private.pem.key"                      # <Thing_Name>.private.key
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop