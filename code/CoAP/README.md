# Setup instructions
-The CoAP scripts require Python 3
-Install the aiocoap python module ex: python install aiocoap
-Update COAP portion the ../../properties.json file to specify the CoAP server
 IP address and port

# CoAP Server
The CoAP server code is available code/CoAP/coap_file_transfer_server.py. 

Assuming you have cloned this repo and are in the CoAP folder, you can start the server via:

python3 coap_fie_transfer_server.py

This wil launch the CoAP server on the configured port and begin listening for CoAP file requests at the URI: 
/file?name=<100B, 10KB, 1MB, 10MB>

# CoAP Client
The CoAP client code is available code/CoAP/coap_file_transfer_client.py. 

Assuming you have cloned this repo and are in the CoAP folder, you can start the
client via:

python3 coap_fie_transfer_client.py

All required tests will and provide the following results:
1) Per file transfer results and summaries to the terminal window
2) Received files will be located at code/CoAP/ReceivedFiles/
3) Average file transfer rate and standard deviation at at code/CoAP/Report/processed_stats.csv

# Wireshark
We use wireshark to capture the packets while we run the client and server code using the capture filter: "host xx.xx.xx.xx", where xx.xx.xx.xx is replaced by the server ip address.

1 capture session must correspond to 1 file. Ex: Run 10000 100B file, not 10000 100 B and 1000 KB together.

These results must be saved to the "/coap/captures/" folder

# Processing Wireshark
Wireshark captures are processed via shark.py

Uses the pyshark library

Set "capture" in main() to the name of the capture file to process

Set "file" in main() to the name of the file you captured (This is only used to name the output results file, simply call it 100B or whatever file you captured, do not give a path) 

Output will be written to a csv file in the "/coap/wireshark_results/" folder (make sure this exists before running)

Will take minutes to process longer captures, especially for 10MB transfers

# Collecting Results
Processing the wireshark captures results in csv files in the "/coap/wireshark_results/" folder

To get statistics run data.py

Needs numpy and matplotlib

Set the "file" in main() to the name of the results file output from shark.py (file name only not path, must be in /coap/wireshark_results/ folder)
