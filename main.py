import csv

# "Host","Log Name","Date Time","Time Zone","Method","URL","Response Code","Bytes Sent","Referer","User Agent"
log_list = []
file_list = ['210725.csv','210802.csv','210808.csv','210815.csv','test.csv']
for file in file_list:
    with open('data/'+file, newline='') as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            log_list.append({
                "host" : row[0],
                "dateTime" : row[2],
                "method" : row[4],
                "url" : row[5],
                "responseCode" : row[6],
                "byteSent" : row[7],
                "referer" :row[8] 
            })


# print(len(log_list))
for log in log_list:
    print(log)
# print(log_list)