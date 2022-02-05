Python comes with a built in http server that we can use to host the files.
The server can be launched via "server.sh" which will start the http server in the folder containing the data files at a specific port. These parameters are specified in the "server.sh" scrupt.

Allow exe permissions:
chmod +x server.sh

Run the server:
./server.sh

If you are running this on your local computer, you can visit http://127.0.0.1:8000/ (8000 is the default port #) to see the list of files available for download.

Set the file and nTimes variables in client.py and run to run the client

