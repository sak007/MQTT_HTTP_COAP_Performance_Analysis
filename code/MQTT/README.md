# Setup instructions
-Install and start the Mosquitto MQTT Broker from https://mosquitto.org/download/ following the directions required for your computing environment. 
-The MQTT scripts require Python 3 and Mosquitto MQTT Broker
-For both your selected subscriber and publisher MQTT systems perform the following steps:
--Install the paho-mqtt python module ex: pip3 install paho-mqtt
--Install the ntplib python module ex: pip3 install ntplib
--Update MQTT portion the ../../properties.json file to specify the MQTT Broker IP address and port

# MQTT Broker
Ensure the MQTT Broker is running on your selected system

# MQTT Subscriber
The MQTT subscriber code is available code/MQTT/mqtt_file_transfer_client.py. 

Assuming you have cloned this repo and are in the MQTT folder, you can start the server via:

python3 main.py -s

This will the start MQTT subscriber and connect to the broker subscibed to the first test (100B / 10000 times / QOS 1). After each test is complete the next will run until all are complete.

For each test a subscriber .csv file showing the file received time stamps will be located in the "Report/" folder. Note, the same process is happening on the publisher.

After all tests are complete, the publiser time stamp files will be sent back to the subscriber, also using MQTT and also placed in the "Report/" folder.

# MQTT Publisher
The MQTT publisher code is available code/MQTT/mqtt_file_transfer_client.py. 

Assuming you have cloned this repo and are in the MQTT folder, you can start the server via:

python3 main.py -p

This will the start MQTT publisher and connect to the broker and begin to publish the first test (100B / 10000 times / QOS 1). After each test is complete the next will run until all are complete.

For each test a publisher .csv file showing the file send start time stamps will be located in the "Report/" folder. 

# Collecting Wireshark
TODO

# Collecting Results
Processing the transfer time captures results in csv files in the "Report/" folder

To get statistics run computeTransferRate.py

python3 computeTransferRate.py

This will generate a file in the "Report/" folder listing the throughput and standard deviation for each test.

Processing the transfer time captures results in csv files in the "" folder

TODO