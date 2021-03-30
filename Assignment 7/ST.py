import paho.mqtt.client as paho
import os
import socket
import ssl
import ast
import datetime as dt
import random as r
import json

def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # Subscribe to all topics
    client.subscribe("Topic3", 1)


def on_message(client, userdata, msg):
    # Func for receiving msgs
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))
    
    previous_data = ast.literal_eval(
        msg.payload.decode("utf-8")
    )
    json_data = dict()
    temp = round(r.uniform(25, 35), ndigits=2)
    hum = round(r.uniform(85, 100), ndigits=2)
    json_data["previous_data_4"] = previous_data
    json_data["temperature"] = temp
    json_data["humidity"] = hum
    json_data["client_name"] = clientId
    payload_json = json.dumps(json_data)
    # topic: temperature # Publishing Temperature values
    client.publish("Topic4", payload_json, qos=1)
    # dyanmodb = boto3.resource("dynamodb", endpoint_url="")
    print("msg sent: Group4")  # Print sent temperature msg on console
    print(payload_json)



mqttc = paho.Client()                                       # mqttc object
# assign on_connect func
mqttc.on_connect = on_connect
# assign on_message func
mqttc.on_message = on_message
#mqttc.on_log = on_log

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
keyPath = "../Creds/{}".format("16012f240a-private.pem.key")
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# connect to aws server
mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_forever()

