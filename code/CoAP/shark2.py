import pyshark
import os 

SERVER = "192.168.0.110"
CLIENT = "192.168.0.229"

def getSourceIP(packet):
    return packet.ip.addr

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
    lastblock = 0
    length = 0
    content = 0
    for packet in cap: # for each packet
        pass
        # if packet.highest_layer == "DATA":
        #     continue
        # continue
        if state == 0 and packet.highest_layer == "COAP": # Found first CoAP packet
            state = 1
            times.append(float(packet.sniff_timestamp))
        # elif state == 0 and packet.highest_layer == "DATA": # Missed a CoAP request packet
        #     print("pass ", i)
        #     continue
        elif state == 1 and packet.highest_layer == "COAP":
            if int(packet.coap.code) == 1: # Request 
                pass
            else: # Block
                #content += packet.coap.block_length
                length += int(packet.length)
        elif state == 1 and packet.highest_layer == "DATA": # Found last CoAP packet
                state = 0
                times[i] = float(packet.sniff_timestamp) - times[i]
                #lengths.append(int(packet.length))
                length += int(packet.length)
                lengths.append(length)
                contents.append(int(packet.data.len))
                print(i)
                i+=1
                length = 0
                
    # Save results 
    print("Message #, total bytes sent, runtime,\n")
    resultsFile = "wireshark_results/results_" + file + ".csv" 
    with open(resultsFile, "w") as f:
        f.write("total bytes,data bytes,header bytes,runtime,\n")
        for j in range(i):
            headerLength = lengths[j] - contents[j]
            print(j, lengths[j], contents[j], headerLength, times[j])
            f.write(str(lengths[j]) + "," + str(contents[j]) + 
                        "," + str(headerLength) + "," + str(times[j]) + ",\n")

def main():
    # Wireshark capture file
    #capture = "100test.pcapng"
    capture = "captures/10KB.pcapng"
    # Corresponding transferred file
    folder = "DataFiles/"
    file = "10KB"  
    processCapture(capture, file)

main()