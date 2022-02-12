from mqtt_file_transfer_client import Client
import argparse
import os

SRC_FILE_PATH = '../../DataFiles/'
DEST_FILE_PATH = 'ReceivedFiles/'

SOURCE_FILES = {'100B': 10000, '10KB': 1000, '1MB': 100, '10MB': 10}
BROKER_ADDR = 'localhost'
BROKER_PORT = 1883

def mqtt_sub(qos):
    client = Client(BROKER_ADDR, BROKER_PORT, 'subscriber')
    client.connect()
    os.makedirs(os.path.dirname('ReceivedFiles/'), exist_ok=True)
    for f in SOURCE_FILES.keys():
        print ("Waiting for " + f)
        client.subscribe(DEST_FILE_PATH + f, 'topic1', qos, SOURCE_FILES[f])
    client.disconnect()

def mqtt_pub(qos):
    client = Client(BROKER_ADDR, BROKER_PORT, 'publisher')
    client.connect()
    for f in SOURCE_FILES.keys():
        print ("Sending " + f)
        client.publish(SRC_FILE_PATH + f, 'topic1', qos, SOURCE_FILES[f])
    client.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "MQTT File Transfer Client")
    parser.add_argument("-s", "--subscriber", help="Run Client as Subscriber.", action="store_true")
    parser.add_argument("-p", "--publisher", help="Run Client as Publisher.", action="store_true")

    args = parser.parse_args()

    if args.subscriber:
        mqtt_sub(1);
        mqtt_sub(2);
    elif args.publisher:
        mqtt_pub(1);
        mqtt_pub(2);
