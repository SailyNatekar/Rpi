# importing libraries
import paho.mqtt.client as paho
import os.path
import socket
import ssl
import csv
import json 
import datetime

def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Saily-1 Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("star" , 1 )                              # Subscribe to all topics
 
def on_message(client, userdata, msg):                      # Func for receiving msgs
    print("topic: "+msg.topic)
    
    msg = json.loads(msg.payload)
    
    sensor = list(msg.keys())[0]
    
    if option == 2:
        msg["source"] = source
        msg["destination"] = destination
    
    print("payload: "+str(msg))
    time = msg[sensor]["time"]
    height = msg[sensor]["height"]
    pressure = msg[sensor]["pressure"]
    fileExists = os.path.isfile('subscriber1.csv')
    with open('subscriber1.csv', 'a') as file:
        headerFields = ['sensor', 'time', 'height', 'pressure']
        writer = csv.DictWriter(file, fieldnames = headerFields)
        if not fileExists:
            writer.writeheader()
        writer.writerow({'sensor': sensor, 'time': time, 'height': height, 'pressure': pressure})
    newmsg = dict()
    jsonnewmsg = dict()
    newmsg["time"] = msg[sensor]["time"]
    newmsg["height"] = msg[sensor]["height"]
    newmsg["pressure"] = msg[sensor]["pressure"]
    if option == 2:
        newmsg["source"] = source
        newmsg["destination"] = destination
    jsonnewmsg["Saily-1"] = newmsg
    payloadmsg = json.dumps(jsonnewmsg)
    mqttc.publish("topic", payloadmsg, qos=1)
#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))

print("1. Get data from all sources.\n2. Transfer Data.") 
option = int(input("Enter the number for performing the operation: ")) 
source = None
destination = None
if option == 2:
    source = input("Enter Source: ")
    destination = input("Enter Destination: ")

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
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop

