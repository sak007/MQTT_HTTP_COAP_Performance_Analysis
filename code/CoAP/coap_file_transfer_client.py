import asyncio
import json
import time
import statistics
import os
from aiocoap import *

class Client:
    def __init__(self, server_addr, server_port):
        self.server_addr = server_addr
        self.server_port = server_port
        self.clear_stats()

    def get_file(self, file_name, file_path, num_retrieves):
        asyncio.run(self.get_file_async(file_name, file_path, num_retrieves))

    async def get_file_async(self, file_name, file_path, num_retrieves):
        num_times_to_loop = num_retrieves

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        while num_times_to_loop > 0:
            protocol = await Context.create_client_context()
            transfer_start_time_ms = time.time_ns() / 1_000_000 # Record transfer start time in ms

            num_times_to_loop -= 1
            request = Message(code=GET, uri='coap://' + self.server_addr + ':' + str(self.server_port) + '/file?name='+file_name)
            try:
                response = await protocol.request(request).response
            except Exception as e:
                print('Failed to fetch resource:')
                print(e)
            else:
                # Calculate transfer time in seconds
                self.transfer_times_sec.append(((time.time_ns() / 1_000_000 ) - transfer_start_time_ms) / 1000) 
                # Store payload size in bytes
                self.transfer_sizes_bytes.append(len(response.payload))
                # Calculate transfer rate in kilobits/sec (kbps)
                self.transfer_rates_kbps.append((self.transfer_sizes_bytes[self.transfer_count] * 8 / 1024) / self.transfer_times_sec[self.transfer_count])
                self.transfer_count += 1

                # Write the payload
                fout=open(file_path + file_name,"wb")
                fout.write(response.payload)
                fout.close()

                print("Received File " + file_name + " (Bytes: %d) (Copy %d of %d): %f sec, %f kbps" %(self.transfer_sizes_bytes[self.transfer_count-1], num_retrieves - num_times_to_loop, num_retrieves, self.transfer_times_sec[self.transfer_count-1], self.transfer_rates_kbps[self.transfer_count-1]))
            await protocol.shutdown()



    def clear_stats(self):
        self.transfer_count = 0
        self.transfer_sizes_bytes = []
        self.transfer_times_sec = []
        self.transfer_rates_kbps = []

    def get_average_transfer_rate(self):
        return sum(self.transfer_rates_kbps) / len(self.transfer_rates_kbps)

    def get_stdev_transfer_rate(self):
        return statistics.stdev(self.transfer_rates_kbps)

if __name__ == "__main__":
    f = open('../../properties.json')
    properties = json.load(f)
    server_address = properties['COAP']['SERVER_ADDR']
    server_port = properties['COAP']['SERVER_PORT']
    f.close()

    os.makedirs(os.path.dirname("Report/"), exist_ok=True)
    f_stats_out = open("Report/processed_stats.csv", "w")
    f_stats_out.write("Test, Throughput Avg (kbps), Throughput StDev (kbps),\n")

    client = Client(server_address,server_port)

    print("Starting 100B Test:")
    client.get_file("100B", "ReceivedFiles/", 2)
    print("Throughput Avg (kbps): " + str(client.get_average_transfer_rate()))
    print("Throughput StDev (kbps): " + str(client.get_stdev_transfer_rate()))
    f_stats_out.write("100B" + "," + str(client.get_average_transfer_rate()) + "," + str(client.get_stdev_transfer_rate()) + ",\n") 
    client.clear_stats()

    print("\nStarting 10KB Test:")
    client.get_file("10KB", "ReceivedFiles/", 2)
    print("Throughput Avg (kbps): " + str(client.get_average_transfer_rate()))
    print("Throughput StDev (kbps): " + str(client.get_stdev_transfer_rate()))
    f_stats_out.write("10KB" + "," + str(client.get_average_transfer_rate()) + "," + str(client.get_stdev_transfer_rate()) + ",\n") 
    client.clear_stats()

    print("\nStarting 1MB Test:")
    client.get_file("1MB", "ReceivedFiles/", 2)
    print("Throughput Avg (kbps): " + str(client.get_average_transfer_rate()))
    print("Throughput StDev (kbps): " + str(client.get_stdev_transfer_rate()))
    f_stats_out.write("1MB" + "," + str(client.get_average_transfer_rate()) + "," + str(client.get_stdev_transfer_rate()) + ",\n") 
    client.clear_stats()

    print("\nStarting 10MB Test:")
    client.get_file("10MB", "ReceivedFiles/", 2)
    print("Throughput Avg (kbps): " + str(client.get_average_transfer_rate()))
    print("Throughput StDev (kbps): " + str(client.get_stdev_transfer_rate()))
    f_stats_out.write("10MB" + "," + str(client.get_average_transfer_rate()) + "," + str(client.get_stdev_transfer_rate()) + ",\n") 
    client.clear_stats()

    f_stats_out.close()
