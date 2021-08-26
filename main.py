import csv
import datetime
import json
import sys

# file_path = sys.argv[1]
if len(sys.argv) < 2:
    print("run as > python3 main.py -sql || > python3 main.py -json input.json")
    sys.exit()

elif sys.argv[1]!= "-json" and sys.argv[1] != "-sql":
    print("No such parameter")
    print("run as > python3 main.py -sql || > python3 main.py -json input.json")

elif (sys.argv[1] == "-sql" and len(sys.argv) < 3):
    print("There is no input file.")
    print("try > python3 main.py -sql input.json")
    sys.exit()

    
order = sys.argv[1]
    






# print("File path : " + file_path)

# "Host","Log Name","Date Time","Time Zone","Method","URL","Response Code","Bytes Sent","Referer","User Agent"

#로그들 들어갈 자리
log_list = []

#data폴더에 있는 애들 중 처리할 아이들
file_list = ['210725.csv','210802.csv','210808.csv','210815.csv','test.csv']

#필터링할 애들 들어갈 곳
url_filtering_dict = {}


#URL 딕셔너리로 하면 안에 있는지 확인 O(1)에 가능해서 리스트보다 성능에 좋음
url_dict = {}

#json 파일 수정해햐암
if order == "-sql":
    with open(sys.argv[2]) as json_file:
        url_dict = json.loads(json_file.read())
    
def writeSQL():
    f = open(str(datetime.datetime.now())+'.sql','a')
    f.write(
        """-- CREATE TABLE AccessLog (
-- 	logAt DATETIME,
-- 	url VARCHAR(2083),
-- 	responseCode INT,
--     referer VARCHAR(2083),
--     method VARCHAR(10),
--     purpose VARCHAR(32),
--     byteSent INT,
-- 	host VARCHAR(20) 
-- );\n\n"""
    )
    for log in log_list:
        _logAt = log['dateTime']
        _host = log['host']
        _referer = log['referer']
        _url = log['url']
        _byteSent = log['byteSent']
        _purpose = log['purpose']
        _reponseCode = log['responseCode']
        _method = log['method']
        query = f'INSERT INTO doraji_log (log_date,gubun,user,IP,data_size) VALUES (\'{_logAt}\',\'{_purpose}\',\'-\',\'{_host}\',{_byteSent});\n'
        f.write(query)


def makeKeyJSON():
    f = open(str(datetime.datetime.now())+'_key.json','a')
    f.write('{\n')
    for key in url_dict.keys():
        # print(key)
        f.write('\t\"'+key+'\" : ,\n')
    f.write('}\n')



for file in file_list:
    with open('data/'+file, newline='') as csvfile:
        readCSV = csv.reader(csvfile)
        if order == "-sql":
            for row in readCSV:

                if 'doraji' in row[8] and row[5] in url_dict:
                    log_list.append({
                        "host" : row[0],
                        "dateTime" : row[2],
                        "method" : row[4],
                        "url" : row[5],
                        "responseCode" : row[6],
                        "byteSent" : row[7],
                        "referer" :row[8],
                        'purpose' : url_dict[row[5]] 
                    })

        elif order =="-json":
            for row in readCSV:
            #여기 조건 수정하세용
                if 'doraji' in row[8] and row[5]!='/' and '*' not in row[5] and '.css' not in row[5] and '.ico' not in row[5] and '.js' not in row[5] and '.png' not in row[5]:
                    url_filtering_dict[row[5]] = "-"
                    # print(row[5])

# key file 생성
if order == "-json":
    makeKeyJSON()

# sql 쿼리문 생성
elif order == "-sql":
    writeSQL()



# 
