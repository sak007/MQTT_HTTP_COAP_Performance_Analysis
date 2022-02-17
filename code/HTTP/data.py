import matplotlib.pyplot as plt
import numpy as np

def extractSizeFromName(filename):
    file = filename[8:-4]
    return file

def extractResults(path):
    with open(path, "r") as f:
        tBytes = [] 
        bBytes = []
        hBytes = []
        runtimes = []
        raw = f.readlines()[1:]
        for line in raw:
            line = line.split(",")
            tBytes.append(int(line[0]))
            bBytes.append(int(line[1]))
            hBytes.append(int(line[2]))
            runtimes.append(float(line[3]))
    return tBytes, bBytes, hBytes, runtimes


def stats(data):
    avg = np.mean(data)
    sd = np.std(data)
    return avg, sd

def main():
    ######## Set These #########################################
    file = "results_10MB.csv" # Results file to process
    ############################################################
    folder = "wireshark_results/" # Wireshark extracted results folder

    fileSize = extractSizeFromName(file)
    print(fileSize)
    tBytes, bBytes, hBytes, runtimes = extractResults(folder + file)

    tRate = [] # transfer rate kilobytes / s
    overhead = [] # file bytes / total bytes sent
    for i in range(len(tBytes)):
        tRate.append((bBytes[i] / 1024) / runtimes[i])
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