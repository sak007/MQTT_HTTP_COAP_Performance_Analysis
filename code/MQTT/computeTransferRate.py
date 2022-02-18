import csv
import statistics
import os

def file(role, data_file, qos):
    return 'Report/' + data_file + '_' + role + '_qos_' + str(qos) + '_stats.csv'

if __name__ == "__main__":
    SOURCE_FILES = ['100B', '10KB', '1MB', '10MB']
    SRC_FILE_PATH = '../../DataFiles/'
    f_stats_out = open("Report/processed_stats.csv", "w")

    f_stats_out.write("Test, QOS, Throughput Avg, Throughput StDev, Total App Layer Avg,\n")

    file_size = {}

    for f in SOURCE_FILES:
        sz = os.path.getsize(SRC_FILE_PATH + f)
        file_size[f] = sz/128


    for i in (1,2):

        for s in SOURCE_FILES:
            start_time = []
            end_time = []
            throughput = []
            # transfer_times = []
            # transfer_rates_kbs = []

            file_name = file('publish', s, i)
            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    start_time.append(float(row[0]))

            file_name = file('subscriber', s, i)
            with open(file_name) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    end_time.append(float(row[0]))

            for st,et in zip(start_time, end_time):
                # print(et - st)
                throughput.append(file_size[s]/(et - st))
            # print(throughput[:50])
            # print(end_time[2],start_time[2])
            # for x in range(len(start_time)):
            #     transfer_times.append(end_time[x] - start_time[x])
            #     transfer_rates_kbs.append(SOURCE_FILES[s] / transfer_times[x])

            f_stats_out.write(s+",") # Test
            f_stats_out.write('QOS' + str(i)+",") # QOS
            f_stats_out.write(str(sum(throughput) / len(throughput))+",") # Throughput Average
            f_stats_out.write(str(statistics.stdev(throughput))+",") # Throughput Standard Deviation
            # f_stats_out.write(str(sum(total_data_over_file_size) / len(total_data_over_file_size))+",") # App Data Overhead
            f_stats_out.write("\n")

            #transfer_time = ((end_time[len(end_time) - 1] - start_time[0]))
            #throughput = SOURCE_FILES[s]/transfer_time
            #print(s + ' QOS' + str(i) + ': ' + str(round((end_time[len(end_time) - 1] - start_time[0]), 2)) + 's')
            #print(throughput)

    f_stats_out.close()
