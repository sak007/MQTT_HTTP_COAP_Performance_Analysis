import asyncio
import json
import time
import statistics
from aiocoap import *

class Client:
    def __init__(self, server_addr, server_port):
        self.server_addr = server_addr
        self.server_port = server_port
        self.clear_stats()

    def get_file(self, file_name, num_retrieves):
        asyncio.run(self.get_file_async(file_name, num_retrieves))

    async def get_file_async(self, file_name, num_retrieves):
        num_times_to_loop = num_retrieves

        while num_times_to_loop > 0:
            protocol = await Context.create_client_context()
            self.transfer_times_ms.append(time.time_ns() / 1_000_000 ) # Record Start Time
            num_times_to_loop -= 1
            request = Message(code=GET, uri='coap://' + self.server_addr + ':' + str(self.server_port) + '/file?name='+file_name)
            try:
                response = await protocol.request(request).response
            except Exception as e:
                print('Failed to fetch resource:')
                print(e)
            else:
                self.transfer_times_ms[self.transfer_count] = ((time.time_ns() / 1_000_000 ) - (self.transfer_times_ms[self.transfer_count])) / 1000
                self.transfer_sizes_bytes.append(len(response.payload))
                self.transfer_rates_kbs.append(self.transfer_sizes_bytes[self.transfer_count] / self.transfer_times_ms[self.transfer_count] / 1000)
                self.transfer_count += 1
                if num_times_to_loop == 1:
                    # Just write it out the last time, we aren't validating the speed of the drive
                    fout=open("out_file","wb")
                    fout.write(response.payload)
                    fout.close()
                print("Received File " + file_name + " (Bytes: %d) (Copy %d of %d): %f sec, %f bytes/sec" %(self.transfer_sizes_bytes[self.transfer_count-1], num_retrieves - num_times_to_loop, num_retrieves, self.transfer_times_ms[self.transfer_count-1], self.transfer_rates_kbs[self.transfer_count-1]))
            await protocol.shutdown()



    def clear_stats(self):
        self.transfer_count = 0
        self.transfer_sizes_bytes = []
        self.transfer_times_ms = []
        self.transfer_rates_kbs = []

    def get_average_transfer_rate(self):
        return sum(self.transfer_rates_kbs) / len(self.transfer_rates_kbs)
        #stdev

    def get_stdev_transfer_rate(self):
        return statistics.stdev(self.transfer_rates_kbs)

if __name__ == "__main__":
    f = open('../../properties.json')
    properties = json.load(f)
    server_address = properties['COAP']['SERVER_ADDR']
    server_port = properties['COAP']['SERVER_PORT']
    f.close()

    client = Client(server_address,server_port)
    client.get_file("100B", 10000)
    print(client.get_average_transfer_rate())
    print(client.get_stdev_transfer_rate())
    client.clear_stats()
    client.get_file("10KB", 1000)
    print(client.get_average_transfer_rate())
    print(client.get_stdev_transfer_rate())
    client.clear_stats()
    client.get_file("1MB", 100)
    print(client.get_average_transfer_rate())
    print(client.get_stdev_transfer_rate())
    client.clear_stats()
    client.get_file("10MB", 10)
    print(client.get_average_transfer_rate())
    print(client.get_stdev_transfer_rate())
    client.clear_stats()
