import time
import requests


def bytesInHeader(header):
    total = 0
    #print("Header")
    #print(header)
    for key in header:
        print(key, header[key])
        total += len(header[key]) + len(key)
    return total

def bytesInBody(body):
    return len(body)

# Are these really the right things to meausre
# Headers are strange
# Content may be compressed and decompressed so what we are getting
# may be high
# Also should we be running from scratch?
def bytesInResponse(response):
    hBytes = bytesInHeader(response.headers)
    bBytes = bytesInBody(response.content)
    return hBytes, bBytes




def client(url):
    runtime = time.time()
    #resp = requests.get("http://127.0.0.1:8000/100B")
    resp = requests.get(url)
    runtime = time.time() - runtime
    hBytes, bBytes = bytesInResponse(resp)
    print(hBytes, bBytes)
    print(runtime)
    return runtime, hBytes, bBytes


def main():
    #host = '127.0.0.1' # Local
    
    ###### Set These ####################
    host = '192.168.0.110'
    nTimes = 10
    file = "10MB"
    #####################################

    port = 8000
    url = "http://" + host + ":" + str(port) + "/" + file
    

    resultsFile = "results/results2_" + file + ".csv" 
    with open(resultsFile, "w") as out:
        out.write("runtime,header bytes, body bytes\n")
        for i in range(nTimes):
            runtime, hBytes, bBytes = client(url)
            time.sleep(.01)

            if i == 0: # Dont save the first download
                continue
            print(i,  "{:.4f}".format(runtime))
            line = str(runtime) + "," + str(hBytes) + "," + str(bBytes) + ",\n"
            out.write(line)
            

if __name__ == "__main__":
    #client("http://192.168.0.110:8000/100B")
    main()