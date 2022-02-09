import paho.mqtt.client as mqtt #pip3 install paho-mqtt
import argparse
import os
import sys
import math
import time

# ---------------------
# Function definitions

# Helper function to ensure value is greater than zero.
def check_non_negative(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError("%s is an invalid value. Value cannot be less than 0." % value)
    return ivalue

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.is_connected_flag = True

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QOS: " + str(granted_qos[0]))
    client.is_subscribed_flag = True

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
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
    header_size += len(args.topic) # Topic
    header_size += 2 # Message id field

    fo_stats.write(str(time.time()) + "," + str(payload_length + header_size) + "\n")
    fout=open(args.file,"wb")
    fout.write(msg.payload)
    fout.close()
    client.num_times_to_loop -= 1
    print("Received File Copy (%d of %d)" %(args.num_times_to_loop-client.num_times_to_loop, args.num_times_to_loop))

def publish_data(topic, payload, qos):
    fo_stats.write(str(time.time())+",\n")
    client.publish_is_complete_flag = False
    client.publish(topic, payload, qos)

def on_publish(client,userdata,result):             #create function for callback
    client.publish_is_complete_flag = True

# ---------------------
# Everything else

# Parse command line arguments
parser = argparse.ArgumentParser(description = "MQTT File Transfer Client")
parser.add_argument("-b", "--broker_address", help = "address of broker", required = False, default = "localhost")
parser.add_argument("-p", "--broker_port", help = "port of broker", required = False, default = "1883")
parser.add_argument("-t", "--type", help = "publisher or subscriber", choices=['publisher', 'subscriber'], required = True, default = "")
parser.add_argument("-f", "--file", help = "Path to input file if publisher or output file if subscriber", required = True, default = "")
parser.add_argument("-c", "--topic", help = "Example: data/files", required = False, default = "data/files")
parser.add_argument("-q", "--qos", help = "Quality of service. Either 0, 1 or 2", choices=['1', '2'], required = False, default = "1")
parser.add_argument("-n", "--num_times_to_loop", help = "Number of times to send or receive file", type=check_non_negative, required = False, default = "1")

args = parser.parse_args()

# Open stats file and clear existing contents
fo_stats = open(args.file + "_" + args.type + "_qos_" + str(args.qos) + "_stats.csv","w")

# Define MQTT Client and connect to Broker
client = mqtt.Client(client_id="MQTT_FT_"+args.type+"_"+str(time.time()), clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

# Add some helper flags to client oject
client.is_connected_flag = False
client.is_subscribed_flag = False
client.publish_is_complete_flag = False
client.num_times_to_loop = args.num_times_to_loop

try:
    client.connect(args.broker_address, int(args.broker_port))
    client.loop_start()
    while not client.is_connected_flag:
        continue
except:
    print("Could not connect to MQTT broker: " + args.broker_address + ":" + args.broker_port)
    sys.exit()

# Start either publisher or client loop
if args.type == "publisher":
    try:
        with open(args.file,"rb") as f:
            file_size = os.path.getsize(args.file)

            while client.num_times_to_loop:
                print("Sent File Copy (%d of %d)" %(args.num_times_to_loop-client.num_times_to_loop+1, args.num_times_to_loop))
                f.seek(0)
                publish_data(args.topic, f.read(file_size), int(args.qos))
                while not client.publish_is_complete_flag:
                    continue
                client.num_times_to_loop -= 1

    except FileNotFoundError:
        print("Cannot open file: " + args.file)
        sys.exit()
else:
    # Subscribing to topic and waiting for SUBACK
    print("Subscribing to topic: " + args.topic + ", QOS:" + args.qos)
    client.subscribe(args.topic, int(args.qos))
    while not client.is_subscribed_flag:
        continue

    # Loop until we've received the required number of file copies
    while client.num_times_to_loop:
        continue

client.disconnect()
client.loop_stop()



