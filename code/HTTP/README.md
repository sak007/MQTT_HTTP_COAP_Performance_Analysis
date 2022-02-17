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
-We use wireshark to capture the packets while we run the client and server code using the capture filter: "host xx.xx.xx.xx", where xx.xx.xx.xx is replaced by the server ip address.
-1 capture session must correspond to 1 file. Ex: Run 10000 100B file, not 10000 100 B and 1000 KB together.
-These results must be saved to the "/http/captures/" folder

# Processing Wireshark
-Wireshark captures are processed via shark.py
-Uses the pyshark library
-Set "capture" in main() to the name of the capture file to process
-Set "file" in main() to the name of the file you captured (This is only used to name the output results file, simply call it 100B or whatever file you captured, do not give a path) 
-Output will be written to a csv file in the "/http/wireshark_results/" folder (make sure this exists before running)
-Will take minutes to process longer captures, especially for 10MB transfers

# Collecting Results
-Processing the wireshark captures results in csv files in the "/http/wireshark_results/" folder
-To get statistics run data.py
-Needs numpy and matplotlib
-Set the "file" in main() to the name of the results file output from shark.py (file name only not path, must be in /http/wireshark_results/ folder)

