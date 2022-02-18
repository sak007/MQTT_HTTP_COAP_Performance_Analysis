import pyshark
import os 
import aiocoap

def getSourceIP(packet):
    return packet.ip.addr

# HTTP Protocal first/last messages 
def isHTTP(packet):
    return packet.protocol == "HTTP"

# Go thru packets sent during http to find out runtimes, num packets and files
# sent by the server. Multiple HTTP requests can be handled
# Sometimes there are more packets if duplicates came in 
def processCapture(capture, file):
    cap = pyshark.FileCapture(capture, only_summaries=False)
    # 0 state means looking for first HTTP message
    # 1 state means going thru HTTP packets
    state = 0 
    lengths = [] # num bytes sent
    contents = [] # Data w/o headers sent in bytes
    times = [] # runtime from first HTTP message to last
    i = 0
    for packet in cap: # for each packet
        if int(packet.number) == 54:
            print(packet.data.tcp_reassembled_length)
            continue
        continue
        if state == 0 and packet.highest_layer == "HTTP": # Found first HTTP packet
            state = 1
            times.append(float(packet.sniff_timestamp))
        elif state == 0 and packet.highest_layer == "DATA": # Missed an HTTP requst packet
            print("pass ", i)
            continue
        elif state == 1 and packet.highest_layer == "DATA": # Found last HTTP packet
                state = 0
                times[i] = float(packet.sniff_timestamp) - times[i]
                lengths.append(int(packet.data.tcp_reassembled_length))
                contents.append(int(packet.http.content_length_header))
                print(i)
                i+=1
        elif state ==1 and packet.highest_layer == "HTTP": # Missed HTTP response packet
            print("pop ", i)
            times.pop()
            state = 1
            times.append(float(packet.sniff_timestamp))
                
    # Save results 
    print("Message #, total bytes sent, runtime,\n")
    resultsFile = "wireshark_results/results_" + file + ".csv"
    print(resultsFile)
    with open(resultsFile, "w") as f:
        f.write("total bytes,data bytes,header bytes,runtime,\n")
        for j in range(i):
            headerLength = lengths[j] - contents[j]
            print(j, lengths[j], contents[j], headerLength, times[j])
            f.write(str(lengths[j]) + "," + str(contents[j]) + 
                        "," + str(headerLength) + "," + str(times[j]) + ",\n")

def main():
    ####### Set These ##############################
    capture = "captures/mqtt.pcapng" # relative capture file path
    file = "10MB" # name of file used (used to name output file)
    ################################################
    processCapture(capture, file)

main()