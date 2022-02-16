# HTTP Server
-Python comes with a built in http server that we can use to host the files.

Assuming you have clone this repo and are in the HTTP folder, you can start the server via:

#Allow exe permissions:
chmod +x server.sh
#Run the server:
./server.sh

This wil launch the server in the HTTP/DataFiles directory on port 8000, making the files in HTTP/DataFiles available.

# HTTP Client
-The http client code is written in HTTP/client.py. This assumes you have installed the requests library.

There are 3 variables that must be set in the main function:
1) host = ip address of ther server - ex: '192.168.0.110'
2) file = name of the file you want to request - ex: '100B'
3) nTimes = the number of times to perform the requeset - ex 10000 for '100B'

# Wireshark
-We use wireshark to capture


Set the file and nTimes variables in client.py and run to run the client

Using wireshark we can determine all of the bytes sent during http requests as well as the runtime.
Before requesting data via client.py, launch wireshark with a capture filter of "host xx.xx.xx.xx", where xx.xx.xx.xx is replaced by the server ip address. This will limit packet capture to only the packets sent and received by the server.
Once all transfers are complete, save the capture file to the captures folder "captures/" and run shark.py to process the data. This will result in a csv file with the results in "wireshark_results/"
These results can then be processed to get the mean and sd via data.py.

