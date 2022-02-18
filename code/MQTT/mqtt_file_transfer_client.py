import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import argparse
import os
import sys
import math
import time
import ntplib #pip3 install ntplib
from queue import Queue

DEST_FILE_PATH = 'ReceivedFiles/'
REPORT_FILE_PATH = 'Report/'

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
        self.time_offset = 0

    def __init__(self, bkr_addr, bkr_port, type):
        self.bkr_addr = bkr_addr
        self.bkr_port = bkr_port
        self.type = type
        self.client = None
        self.time_offset = 0

    # Referenced code from Google example found at:
    # https://www.programcreek.com/python/example/91316/ntplib.NTPClient
    def SyncClockToNtp(self, retries, server):
        """Syncs the hardware clock to an NTP server."""
        attempts = 0
        ntp_client = ntplib.NTPClient()
        response = None

        while True:
            try:
                response = ntp_client.request(server, version=3)
            except:
                print('NTP client request error')
            if response or attempts >= retries:
                break
            time.sleep(3)
            attempts += 1

        self.time_offset = response.offset
        print(self.time_offset)

    def connect(self):
        # Sync system clock to NTP server
        ntp_response = self.SyncClockToNtp(2, "time.google.com")

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
        # if msg.topic.split("/")[0] == 'Report':
        #     fout=open(msg.topic,"wb")
        #     fout.write(msg.payload)
        #     fout.close()
        #     return
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

        fo_stats.write(str(time.time()+self.time_offset) + "," + str(payload_length + header_size) + "\n")

        # Write the file later to allow the function to return
        self.message_queue.put(msg.payload)
        client.num_times_to_loop -= 1
        print("Received File Copy (%d of %d)" %(self.count - client.num_times_to_loop, self.count))

    def publish_data(self, payload):
        if self.file.split("/")[0] != 'Report':
            fo_stats.write(str(time.time()+self.time_offset)+",\n")
        self.client.publish_is_complete_flag = False
        self.client.publish(self.topic, payload, self.qos)

    def on_publish(self, client,userdata,result):             #create function for callback
        client.publish_is_complete_flag = True

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()

    def publish(self, file, topic, qos, count):
        self.file = file
        self.topic = topic
        self.qos = qos
        self.count = count
        self.client.num_times_to_loop = count
        global fo_stats
        filename = REPORT_FILE_PATH + self.file.split("/")[-1] + "_" + "publish" + "_qos_" + str(qos) + "_stats.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fo_stats = open(filename, "w")
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

    def subscribe(self, file, topic, qos, count):
        # self.client = self.connect(self.bkr_addr, self.bkr_port, self.count, "subscriber")
        self.file = file
        self.topic = topic
        self.qos = qos
        self.count = count
        self.client.num_times_to_loop = count
        global fo_stats
        filename = REPORT_FILE_PATH + self.file.split("/")[-1] + "_" + "subscriber" + "_qos_" + str(qos) + "_stats.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fo_stats = open(filename,"w")

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

    def subscribe_report(self, file):
        # self.client = self.connect(self.bkr_addr, self.bkr_port, self.count, "subscriber")
        self.file = file
        self.client.subscribe(file, 2)
        while not self.client.is_subscribed_flag:
            continue


    def publish_report(self, file):
        self.file = file
        try:
            with open(self.file,"rb") as f:
                file_size = os.path.getsize(self.file)
                f.seek(0)
                self.publish_data(f.read(file_size))
        except FileNotFoundError:
            print("Cannot open file: " + self.file)
            sys.exit()

if __name__ == "__main__":

    if True:
    # use this code block for publish
     client = Client('192.168.1.9', 1883, '10MB', 'topic1', 1, 10, 'publisher')
     client.connect()
     client.publish()
    else:
    # Use this code block for client
     client = Client('192.168.1.9', 1883, 'op', 'topic1', 1, 10, 'subscriber')
     client.connect()
     client.subscribe()
