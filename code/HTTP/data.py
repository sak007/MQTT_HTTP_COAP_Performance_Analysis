import matplotlib.pyplot as plt
import numpy as np

def extractSizeFromName(filename):
    file = filename[8:-4]
    return file

def extractResults(path):
    with open(path, "r") as f:
        nPackets = []
        tBytes = [] 
        bBytes = []
        hBytes = []
        runtimes = []
        raw = f.readlines()[1:]
        for line in raw:
            line = line.split(",")
            nPackets.append(int(line[0]))
            tBytes.append(int(line[1]))
            bBytes.append(int(line[2]))
            hBytes.append(int(line[3]))
            runtimes.append(float(line[4]))
    return nPackets, tBytes, bBytes, hBytes, runtimes


def stats(data):
    avg = np.mean(data)
    sd = np.std(data)
    return avg, sd

def main():
    folder = "wireshark_results/"
    file = "results_10MB.csv" ##### File to proces ######
    fileSize = extractSizeFromName(file)
    print(fileSize)
    nPackets, tBytes, bBytes, hBytes, runtimes = extractResults(folder + file)

    tRate = [] # transfer rate kilobytes / s
    overhead = [] # file bytes / total bytes sent
    for i in range(len(nPackets)):
        tRate.append((bBytes[i] / 1000) / runtimes[i])
        overhead.append(tBytes[i] / bBytes[i] )

    rAvg, rSd = stats(runtimes)
    print("runtime avg: ", rAvg, " sd ", rSd)
    tAvg, tSd = stats(tRate)
    oAvg, oSd = stats(overhead)

    print("transfer avg: ", tAvg, " sd ", tSd)
    print("overhead avg: ", oAvg, " sd ", oSd)

    plt.figure()
    plt.title(fileSize + " Transfer Rate")
    plt.hist(tRate)

    plt.show()


if __name__ == "__main__":
    main()