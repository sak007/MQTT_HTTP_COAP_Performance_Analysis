import csv


def file(role, data_file, qos):
    return 'Report/' + data_file + '_' + role + '_qos_' + str(qos) + '_stats.csv'

if __name__ == "__main__":
    SOURCE_FILES = {'100B': 100/1024, '10KB' : 10, '1MB' : 1024, '10MB' : 10240}

    for i in (1,2):

        for s in SOURCE_FILES.keys():
            start_time = []
            end_time = []
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


            # for s,e in zip(start_time, end_time):
            #     print((float(e) - float(s)) * 1000)
            transfer_time = ((end_time[len(end_time) - 1] - start_time[0]))
            throughput = SOURCE_FILES[s]/transfer_time
            print(s + ' QOS' + str(i) + ': ' + str(round((end_time[len(end_time) - 1] - start_time[0]), 2)) + 's')
            print(throughput)
