import datetime
import os
import json
import asyncio
import aiocoap.resource as resource
import aiocoap

SRC_FILE_PATH = '../../DataFiles/'
SOURCE_FILES = ['100B', '10KB', '1MB', '10MB']

class FileResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.files = {}
        for f in SOURCE_FILES:
            try:
                f_handle = open(SRC_FILE_PATH + f, "rb")
                f_size = os.path.getsize(SRC_FILE_PATH + f)
                self.files[f] = f_handle.read(f_size)
                f_handle.close()
                print("Pre loaded file: " + SRC_FILE_PATH + f + ", size: " + str(f_size) + " bytes.")
            except:
                print("Failed to open file: " + SRC_FILE_PATH + f)

    async def render_get(self, request):
        for uri_param in request.opt.uri_query:
            if uri_param.find("name=") != -1:
                file_name = uri_param.split('=')[1]
                if file_name in self.files.keys():
                    print ("Sending file requested: " + file_name)
                    return aiocoap.Message(payload=self.files[file_name])
                else:
                    print ("File requested not found: " + file_name)
                    return aiocoap.Message(payload=bytes("ERROR: File requested not found: " + file_name, "utf-8"))

        return aiocoap.Message(payload=b"ERROR: Bad Request")

async def main():
    f = open('../../properties.json')
    properties = json.load(f)
    server_address = properties['COAP']['SERVER_ADDR']
    server_port = properties['COAP']['SERVER_PORT']
    f.close()

    # Resource tree creation
    root = resource.Site()
    root.add_resource(['file'], FileResource())

    await aiocoap.Context.create_server_context(bind=(server_address,server_port),site=root)

    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())