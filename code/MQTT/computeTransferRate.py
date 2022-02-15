import csv
import statistics

def file(role, data_file, qos):
    return 'Report/' + data_file + '_' + role + '_qos_' + str(qos) + '_stats.csv'

if __name__ == "__main__":
    SOURCE_FILES = {'100B': 0.1, '10KB' : 10, '1MB' : 1024, '10MB' : 10240}
    f_stats_out = open("Report/processed_stats.csv", "w")
    
    f_stats_out.write("Test, QOS, Throughput Avg, Throughput StDev, Total App Layer Avg,\n")

    for i in (1,2):

        for s in SOURCE_FILES.keys():
            start_time = []
            end_time = []
            total_data_over_file_size = []
            transfer_times = []
            transfer_rates_kbs = []

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
                    total_data_over_file_size.append((float(row[1])/1000) / SOURCE_FILES[s])

            for x in range(len(start_time)):
                transfer_times.append(end_time[x] - start_time[x])
                transfer_rates_kbs.append(SOURCE_FILES[s] / transfer_times[x])

            f_stats_out.write(s+",") # Test
            f_stats_out.write(str(i)+",") # QOS
            f_stats_out.write(str(sum(transfer_rates_kbs) / len(transfer_rates_kbs))+",") # Throughput Average
            f_stats_out.write(str(statistics.stdev(transfer_rates_kbs))+",") # Throughput Standard Deviation
            f_stats_out.write(str(sum(total_data_over_file_size) / len(total_data_over_file_size))+",") # App Data Overhead 
            f_stats_out.write("\n")

            # for s,e in zip(start_time, end_time):
            #     print((float(e) - float(s)) * 1000)
            #transfer_time = ((end_time[len(end_time) - 1] - start_time[0]))
            #throughput = SOURCE_FILES[s]/transfer_time
            #print(s + ' QOS' + str(i) + ': ' + str(round((end_time[len(end_time) - 1] - start_time[0]), 2)) + 's')
            #print(throughput)

    f_stats_out.close()
