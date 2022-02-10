import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import argparse
import os
import sys
import math
import time
from queue import Queue



class Client:

    def __init__(self, bkr_addr, bkr_port, file, topic, qos, count, type):
        self.bkr_addr = bkr_addr
        self.bkr_port = bkr_port
        self.file = file
        self.topic = topic
        self.qos = qos
        self.count = count
        self.type = type
        self.client = None

    def connect(self):
        # Define MQTT Client and connect to Broker
        self.client = mqtt.Client(client_id="MQTT_FT_"+self.type+"_"+str(time.time()), clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

        # Add some helper parameters to client oject
        self.client.is_connected_flag = False
        self.client.is_subscribed_flag = False
        self.client.publish_is_complete_flag = False
        self.client.num_times_to_loop = self.count
        self.message_queue = Queue()

        try:
            self.client.connect(self.bkr_addr, self.bkr_port)
            self.client.loop_start()
            while not self.client.is_connected_flag:
                continue
        except:
            print("Could not connect to MQTT broker: " + self.bkr_addr + ":" + self.bkr_port)
            sys.exit()


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.is_connected_flag = True

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed with QOS: " + str(granted_qos[0]))
        client.is_subscribed_flag = True

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        payload_length = len(msg.payload)

        # Fixed Header
        header_size = 1 # Control Byte

        if payload_length < 2 ** 7:
            header_size += 1 # Packet Length < 128: 1 byte
        elif payload_length < 2 ** 14:
            header_size += 2 # Packet Length >= 128 < 16383: 2 bytes
        elif payload_length < 2 ** 21:
            header_size += 3 # Packet Length >= 16384 < 2097151: 3 bytes
        else:
            header_size += 4 # Packet Length >= 2097151 < 268435455: 4 bytes

        # Variable Header
        header_size += 2 # Fixed topic length field
        header_size += len(self.topic) # Topic
        header_size += 2 # Message id field

        fo_stats.write(str(time.time()) + "," + str(payload_length + header_size) + "\n")

        # Write the file later to allow the function to return 
        self.message_queue.put(msg.payload)
        client.num_times_to_loop -= 1
        print("Received File Copy (%d of %d)" %(self.count - client.num_times_to_loop, self.count))

    def publish_data(self, payload):
        fo_stats.write(str(time.time())+",\n")
        self.client.publish_is_complete_flag = False
        self.client.publish(self.topic, payload, self.qos)

    def on_publish(self, client,userdata,result):             #create function for callback
        client.publish_is_complete_flag = True

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self):
        # self.client = self.connect()
        global fo_stats
        fo_stats = open(self.file + "_" + "publish" + "_qos_" + str(1) + "_stats.csv","w")
        try:
            with open(self.file,"rb") as f:
                file_size = os.path.getsize(self.file)

                while self.client.num_times_to_loop:
                    print("Sent File Copy (%d of %d)" %(self.count-self.client.num_times_to_loop+1, self.count))
                    f.seek(0)
                    self.publish_data(f.read(file_size))
                    while not self.client.publish_is_complete_flag:
                        continue
                    self.client.num_times_to_loop -= 1

        except FileNotFoundError:
            print("Cannot open file: " + self.file)
            sys.exit()
        self.disconnect()

    def subscribe(self):
        # self.client = self.connect(self.bkr_addr, self.bkr_port, self.count, "subscriber")
        global fo_stats
        fo_stats = open(self.file + "_" + "subscriber" + "_qos_" + str(1) + "_stats.csv","w")

        # Subscribing to topic and waiting for SUBACK
        print("Subscribing to topic: " + self.topic + ", QOS:" + str(self.qos))
        self.client.subscribe(self.topic, self.qos)
        while not self.client.is_subscribed_flag:
            continue

        # Loop until we've received and written the required number of file copies
        while (self.client.num_times_to_loop > 0) or (not self.message_queue.empty()):
            message_payload = self.message_queue.get()
            if not message_payload is None:
                fout=open(self.file,"wb")
                fout.write(message_payload)
                fout.close()
            continue

        self.disconnect()


if __name__ == "__main__":

    if True:
    # use this code block for publish
     client = Client('localhost', 1883, '10MB', 'topic1', 1, 10, 'publisher')
     client.connect()
     client.publish()
    else: 
    # Use this code block for client
     client = Client('localhost', 1883, 'op', 'topic1', 1, 10, 'subscriber')
     client.connect()
     client.subscribe()
