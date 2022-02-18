import os
import pyshark

def getSourceIP(packet):
    return packet.ip.addr

# First message sent by server
def isMQTTLayer(packet):
    return packet.highest_layer == "MQTT"

def isMQTTPublish(packet):
    return packet.mqtt.msgtype == "3" or packet.mqtt.msgtype == "6"

def isFromPublisher(packet):
    return packet.ip.addr == '192.168.1.119'

def calcMQTTMsgLength(packet):
    # Fixed Header
    # print(packet)
    # print(packet.tcp.len)
    if hasattr(packet, 'data'):
        return int(packet.data.tcp_reassembled_length)
    return int(packet.tcp.len)

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
    file_size = {
        'data/files/100B': os.path.getsize('../../DataFiles/100B'),
        'data/files/10KB': os.path.getsize('../../DataFiles/10KB'),
        'data/files/01MB': os.path.getsize('../../DataFiles/1MB'),
        'data/files/10MB': os.path.getsize('../../DataFiles/10MB')
        }

    length = 0
    packets_list = []
    topic = ''
    for packet in cap:
        if isMQTTLayer(packet):
            if isMQTTPublish(packet) and isFromPublisher(packet):
                if packet.mqtt.msgtype == '3':
                    if length != 0:
                        x = (topic + ',' + str(length))
                        print(x)
                        packets_list.append(x)
                    topic = packet.mqtt.topic + '_QOS_' + packet.mqtt.qos
                    length = 0
                length += calcMQTTMsgLength(packet)

                
    if length != 0:
        packets_list.append(topic + ',' + str(length))
    mqtt_summary = set(packets_list)
    print(mqtt_summary)

    

def main():
    capture = "Report/wireshark.pcapng"
    file = "wireshark_capture_processed.csv"
    processCapture(capture, file)

main()
