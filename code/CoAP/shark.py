import pyshark
import os 
import aiocoap

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
    length = 0

    for packet in cap: # for each packet
        # First Coap Packet
        if state == 0 and packet.highest_layer == "COAP":
            state = 1
            times.append(float(packet.sniff_timestamp)) # start time
        # Handle CoAP Blocks
        elif state == 1 and packet.highest_layer == "COAP":
            if int(packet.coap.code) == 1: # CoAP Request 
                pass
            else: # CoAP Block Message
                # CoAP payload + header = # bytes in UDP payload
                l = len(packet.udp.payload.split(":"))
                length += l
                #c = len(packet.coap.block_payload.split(":"))
                #print(l, c, l - c)
                #print(length)
        # Last CoAP Packet
        elif state == 1 and packet.highest_layer == "DATA": 
                times[i] = float(packet.sniff_timestamp) - times[i] # end time
                # CoAP payload + header = # bytes in UDP payload
                l = len(packet.udp.payload.split(":"))
                length += len(packet.udp.payload.split(":"))
                #c = len(packet.coap.block_payload.split(":"))
                #print(l, c, l - c)
                lengths.append(length)
                contents.append(int(packet.data.len))

                print(i)
                i+=1
                length = 0
                state = 0
                
    
    # Save results 
    if not os.path.exists("wireshark_results"):
        os.mkdir("wireshark_results")
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
    ####### Set These ##############################
    capture = "captures/10MB.pcapng" # relative capture file path
    file = "10MB" # name of file used (used to name output file)
    ################################################
    processCapture(capture, file)

main()