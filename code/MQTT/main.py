from mqtt_file_transfer_client import Client
import argparse
import os
import json
import time

SRC_FILE_PATH = '../../DataFiles/'
DEST_FILE_PATH = 'ReceivedFiles/'
SOURCE_FILES = {'100B': 0, '10KB': 10, '1MB': 0, '10MB': 0}
TOPICS = {'100B': 'data/files/100B', '10KB': 'data/files/10KB', '1MB': 'data/files/01MB', '10MB': 'data/files/10MB'}
RTOPICS = {'100B': 'report/files/100B', '10KB': 'report/files/10KB', '1MB': 'report/files/01MB', '10MB': 'report/files/10MB'}

def mqtt_sub(qos):
    client = Client(BROKER_ADDR, BROKER_PORT, 'subscriber')
    client.connect()
    os.makedirs(os.path.dirname('ReceivedFiles/'), exist_ok=True)
    for f in SOURCE_FILES.keys():
        if SOURCE_FILES[f] == 0:
            continue
        print ("Waiting for " + f)
        client.subscribe(DEST_FILE_PATH + f, TOPICS[f], qos, SOURCE_FILES[f])
    client.disconnect()

def mqtt_pub(qos):
    client = Client(BROKER_ADDR, BROKER_PORT, 'publisher')
    client.connect()
    for f in SOURCE_FILES.keys():
        if SOURCE_FILES[f] == 0:
            continue
        print ("Sending " + f + ". Starting in 30 seconds.")
        time.sleep(10)
        client.publish(SRC_FILE_PATH + f, TOPICS[f], qos, SOURCE_FILES[f])
    client.disconnect()

def request_report():
    client = Client(BROKER_ADDR, BROKER_PORT, 'subscriber')
    client.connect()
    os.makedirs(os.path.dirname('Report/'), exist_ok=True)
    qos = 1
    client.subscribe_report('Report/' + f + '_subscriber_qos_' + str(qos) + '_stats')
    client.disconnect()

def send_report():
    client = Client(BROKER_ADDR, BROKER_PORT, 'publisher')
    client.connect()
    client.publish_report()
    client.disconnect()

def send_results():
    client = Client(BROKER_ADDR, BROKER_PORT, 'publisher')
    client.connect()
    for i in (1,2):
        for f in SOURCE_FILES.keys():
            file = 'Report/' + f + '_subscriber_qos_' + str(i) + '_stats.csv'
            print ("Sending " + file + ". Starting in 30 seconds.")
            client.publish(file, file, 2, 1)
            time.sleep(10)
    client.disconnect()

def request_results():
    client = Client(BROKER_ADDR, BROKER_PORT, 'subscriber')
    client.connect()
    os.makedirs(os.path.dirname('ReceivedFiles/'), exist_ok=True)
    for i in (1,2):
        for f in SOURCE_FILES.keys():
            file = 'Report/' + f + '_subscriber_qos_' + str(i) + '_stats.csv'
            client.subscribe(file, file, 2, 1)
    client.disconnect()


def init():
    f = open('../../properties.json')
    properties = json.load(f)
    global BROKER_ADDR
    BROKER_ADDR = properties['MQTT']['BROKER_ADDR']
    global BROKER_PORT
    BROKER_PORT = properties['MQTT']['BROKER_PORT']

if __name__ == "__main__":
    init()
    parser = argparse.ArgumentParser(description = "MQTT File Transfer Client")
    parser.add_argument("-s", "--subscriber", help="Run Client as Subscriber.", action="store_true")
    parser.add_argument("-p", "--publisher", help="Run Client as Publisher.", action="store_true")

    args = parser.parse_args()

    if args.subscriber:
        # mqtt_sub(1)
        # mqtt_sub(2)
        send_results()
    elif args.publisher:
        # mqtt_pub(1)
        # mqtt_pub(2)
        request_results()
