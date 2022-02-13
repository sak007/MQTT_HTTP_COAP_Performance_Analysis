Python comes with a built in http server that we can use to host the files.
The server can be launched via "server.sh" which will start the http server in the folder containing the data files at a specific port. These parameters are specified in the "server.sh" scrupt.

Allow exe permissions:
chmod +x server.sh

Run the server:
./server.sh

If you are running this on your local computer, you can visit http://127.0.0.1:8000/ (8000 is the default port #) to see the list of files available for download.

Set the file and nTimes variables in client.py and run to run the client

Using wireshark we can determine all of the bytes sent during http requests as well as the runtime.
Before requesting data via client.py, launch wireshark with a capture filter of "host xx.xx.xx.xx", where xx.xx.xx.xx is replaced by the server ip address. This will limit packet capture to only the packets sent and received by the server.
Once all transfers are complete, save the capture file to the captures folder "captures/" and run shark.py to process the data. This will result in a csv file with the results in "wireshark_results/"
These results can then be processed to get the mean and sd via data.py.

