#ip.addr == 192.168.7.193 and tcp.port == 1883
import pyshark

#capture = pyshark.LiveCapture(interface='en0', bpf_filter="ip.addr == 192.168.7.193 and tcp.port == 1883")

# Example code from stack overflow: https://stackoverflow.com/questions/57099396/continuously-capture-packets-in-pyshark

#for packet in capture.sniff_continuously():
#    print('Just arrived:', packet)

import pyshark

SERVER = "192.168.7.193"
CLIENT = "192.168.7.246"

def getSourceIP(packet):
    return packet.ip.addr

# First message sent by server
def isMQTTLayer(packet):
    return packet.highest_layer == "MQTT"

def isMQTTPublish(packet):
    return packet.mqtt.msgtype == "3"

def calcMQTTMsgLength(packet):
    # Fixed Header
    fixed_header_size = 1 # Header Control Byte
    message_length = int(packet.mqtt.len) # Message Length

    if message_length < 2 ** 7:
        fixed_header_size += 1 # Message Length < 128: 1 byte
    elif message_length < 2 ** 14:
        fixed_header_size += 2 # Message Length >= 128 < 16383: 2 bytes
    elif message_length < 2 ** 21:
        fixed_header_size += 3 # Message Length >= 16384 < 2097151: 3 bytes
    else:
        fixed_header_size += 4 # Message Length >= 2097151 < 268435455: 4 bytes

    return fixed_header_size + message_length


# Last message sent in HTTP by server
def isDataLayer(packet):
    return packet.highest_layer == "DATA"

# Number of file bytes transfered
def getNumContentBytes(packet):
    return int(packet.mqtt.content_length)

def processCapture(capture, file):
    
    cap = pyshark.FileCapture(capture)
    state = 0
    counts = []
    lengths = []
    dataLengths = []
    i = 0
    length = 0
    mqtt_summary = {}
    for packet in cap:
        if isMQTTLayer(packet):
            if isMQTTPublish(packet):
                print("MID:" + packet.mqtt.msgid + " Topic: " + packet.mqtt.topic + ", QOS: " + packet.mqtt.qos + " Length: " + str(calcMQTTMsgLength(packet)))
                if packet.mqtt.qos not in mqtt_summary.keys():
                    mqtt_summary[packet.mqtt.qos] = {}
                if packet.mqtt.topic not in mqtt_summary[packet.mqtt.qos].keys():
                    mqtt_summary[packet.mqtt.qos][packet.mqtt.topic] = {}
                    mqtt_summary[packet.mqtt.qos][packet.mqtt.topic]["count"] = 0
                    mqtt_summary[packet.mqtt.qos][packet.mqtt.topic]["total_length"] = 0

                mqtt_summary[packet.mqtt.qos][packet.mqtt.topic]["count"] += 1
                mqtt_summary[packet.mqtt.qos][packet.mqtt.topic]["total_length"] += calcMQTTMsgLength(packet)

    print(mqtt_summary)

#                print(vars(packet.mqtt))
        #            print(packet.mqtt.msgtype)
            #print(vars(packet.mqtt))
            #quit()
            #print("Topic: "+packet.mqtt.topic_len)
            #i=i+1
#    print("Message #, # packets sent, total bytes sent, data bytes sent, header bytes sent")
    
#    resultsFile = "wireshark/results_" + file + ".csv" 
#    with open(resultsFile, "w") as f:
#        f.write("# packets,total bytes,data bytes,header bytes\n")
#        for j in range(i):
#            headerLength = lengths[j] - dataLengths[j]
#            print(j, counts[j], lengths[j], dataLengths[j], headerLength)
#            f.write(str(counts[j]) + "," + str(lengths[j]) + "," + str(dataLengths[j]) + 
#                        "," + str(headerLength) + ",\n")

def main():
    capture = "Report/wireshark_capture.pcapng"
    file = "wireshark_capture_processed.csv"
    processCapture(capture, file)

main()