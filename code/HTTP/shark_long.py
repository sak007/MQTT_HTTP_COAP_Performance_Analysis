import pyshark

SERVER = "192.168.0.110"
CLIENT = "192.168.0.229"

def getSourceIP(packet):
    return packet.ip.addr

# First message sent by server
def isHTTPLayer(packet):
    return packet.highest_layer == "HTTP"

# Last message sent in HTTP by server
def isDataLayer(packet):
    return packet.highest_layer == "DATA"

# Number of file bytes transfered
def getNumContentBytes(packet):
    return int(packet.http.content_length)

def processCapture(capture, file):
    
    cap = pyshark.FileCapture(capture)
    state = 0
    counts = []
    lengths = []
    dataLengths = []
    i = 0
    length = 0
    for packet in cap:
        if state == 0 and isHTTPLayer(packet):
            state = 1
        #     #print(getSourceIP(packet))
            counts.append(0)
            lengths.append(0)
            dataLengths.append(0)
        if state == 1 and getSourceIP(packet) == SERVER:
                
             counts[i] += 1
             lengths[i] += int(packet.length)
             #print(packet.length, lengths[i])
        if state == 1 and isDataLayer(packet):
        #     print(i, counts[i])

            state = 0
        #     #print(getSourceIP(packet))
            dataLengths[i] = getNumContentBytes(packet)
            print(dataLengths[i], lengths[i], counts[i])
            i += 1
    print("Message #, # packets sent, total bytes sent, data bytes sent, header bytes sent")
    
    resultsFile = "wireshark/results_" + file + ".csv" 
    with open(resultsFile, "w") as f:
        f.write("# packets,total bytes,data bytes,header bytes\n")
        for j in range(i):
            headerLength = lengths[j] - dataLengths[j]
            print(j, counts[j], lengths[j], dataLengths[j], headerLength)
            f.write(str(counts[j]) + "," + str(lengths[j]) + "," + str(dataLengths[j]) + 
                        "," + str(headerLength) + ",\n")

def main():
    capture = "10MB.pcapng"
    file = "10MB"
    processCapture(capture, file)

main()