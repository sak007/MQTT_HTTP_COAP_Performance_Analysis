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
We use wireshark to capture packet data and process the results to get the total application data transferred for the
various tests.

Using wireshark we can determine all of the bytes sent during CoAP requests. Before requesting data via 
coap_file_transfer_client.py, launch wireshark with a capture filter of "host xx.xx.xx.xx", where xx.xx.xx.xx is 
replaced by the server ip address. This will limit packet capture to only the packets sent and received by the server.

