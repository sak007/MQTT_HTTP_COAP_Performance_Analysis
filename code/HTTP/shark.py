import pyshark
import os 

SERVER = "192.168.0.110"
CLIENT = "192.168.0.229"

def getSourceIP(packet):
    return packet.ip.addr

# HTTP Protocal first/last messages 
def isHTTP(packet):
    return packet.protocol == "HTTP"

# Go thru packets sent during http to find out runtimes, num packets and files
# sent by the server. Multiple HTTP requests can be handled
# Sometimes there are more packets if duplicates came in 
def processCapture(capture, folder, file):
    cap = pyshark.FileCapture(capture, only_summaries=True)
    # 0 state means looking for first HTTP message
    # 1 state means going thru HTTP packets
    state = 0 
    counts = [] # num packets sent by server
    lengths = [] # num bytes sent
    times = [] # runtime from first HTTP message to last
    i = 0
    for packet in cap: # for each packet
        if state == 0 and packet.protocol == "HTTP": # Found first HTTP packet
            state = 1
            times.append(float(packet.time))
            counts.append(0)
            lengths.append(0)
        # Go thru packets sent by server for http
        if state == 1 and packet.source == SERVER: 
            lengths[i] += int(packet.length)
            counts[i] += 1
            if packet.protocol == "HTTP": # Last HTTP packet
                state = 0
                times[i] = float(packet.time) - times[i]
                i+=1
                print(i)
    # Save results 
    print("Message #, # packets sent, total bytes sent, runtime,\n")
    fileSize = os.path.getsize(folder + file) # transfered file size
    resultsFile = "wireshark_results/results_" + file + ".csv" 
    with open(resultsFile, "w") as f:
        f.write("# packets,total bytes,data bytes,header bytes, runtime,\n")
        for j in range(i):
            headerLength = lengths[j] - fileSize
            print(j, counts[j], lengths[j], fileSize, headerLength, times[j])
            f.write(str(counts[j]) + "," + str(lengths[j]) + "," + str(fileSize) + 
                        "," + str(headerLength) + "," + str(times[j]) + ",\n")

def main():
    # Wireshark capture file
    capture = "100test.pcapng"
    #capture = "captures/10MB.pcapng"
    # Corresponding transferred file
    folder = "DataFiles/"
    file = "100B"  
    processCapture(capture, folder, file)

main()