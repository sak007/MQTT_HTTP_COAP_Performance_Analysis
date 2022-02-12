import matplotlib.pyplot as plt
import numpy as np

def extractSizeFromName(filename):
    file = filename[8:-4]
    return file

def extractResults(path):
    with open(path, "r") as f:
        runtimes = []
        hBytes = []
        bBytes = []
        raw = f.readlines()[1:]
        for line in raw:
            line = line.split(",")
            runtimes.append(float(line[0]))
            hBytes.append(int(line[1]))
            bBytes.append(int(line[2]))
    return runtimes, hBytes, bBytes


def divide(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i]/b[i])
    return c

# Total Bytes / content bytes
def overhead(hBytes, bBytes):
    res = []
    for i in range(len(hBytes)):
        res.append((hBytes[i] + bBytes[i]) / bBytes[i])
    return res

def stats(data):
    avg = np.mean(data)
    sd = np.std(data)
    return avg, sd


def main():
    folder = "results/"
    file = "results_100B.csv"
    fileSize = extractSizeFromName(file)
    print(fileSize)
    runtimes, hBytes, bBytes = extractResults(folder + file)
    transfer = divide(bBytes, runtimes)
    overheadRate = overhead(hBytes, bBytes)
    rAvg, rSd = stats(runtimes)
    print("runtime avg: ", rAvg, " sd ", rSd)
    hAvg, hSd = stats(hBytes)
    print("header avg: ", hAvg, " sd ", hSd)
    bAvg, bSd = stats(bBytes)
    print("body avg: ", bAvg, " sd ", bSd)
    tAvg, tSd = stats(transfer)
    print("transfer avg: ", tAvg, " sd ", tSd)
    oAvg, oSd = stats(overheadRate)
    print("overhead avg: ", oAvg, " sd ", oSd)

    dRate = [] # Data transfer rate
    dhRate = [] # Data + header transfer rate
    for i in range(len(runtimes)):
        dRate.append((bBytes[i] / 1000)/runtimes[i])
        dhRate.append(((bBytes[i] + hBytes[i]) / 1000) / runtimes[i])
    dAvg, dSd = stats(dRate)
    dhAvg, dhSd = stats(dhRate)
    print("Rate (kilobytes / s): mean, sd")
    print("Data only: ", dAvg, dSd)
    print("Data + Header: ", dhAvg, dhSd)

    plt.figure()
    plt.title(fileSize + " Runtime")
    plt.hist(runtimes)

    plt.figure()
    plt.title(fileSize + " Header Bytes")
    plt.hist(hBytes)

    plt.figure()
    plt.title(fileSize + " Body Bytes")
    plt.hist(bBytes)

    plt.figure()
    plt.title(fileSize + " Transfer Rate")
    plt.hist(transfer)

    plt.figure()
    plt.title(fileSize + " Overhead Bytes")
    plt.hist(overheadRate)
    plt.show()


if __name__ == "__main__":
    main()