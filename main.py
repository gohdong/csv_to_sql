import csv
import datetime

# "Host","Log Name","Date Time","Time Zone","Method","URL","Response Code","Bytes Sent","Referer","User Agent"

#로그들 들어갈 자리
log_list = []

#data폴더에 있는 애들 중 처리할 아이들
file_list = ['210725.csv','210802.csv','210808.csv','210815.csv','test.csv']

url_filtering_dict = {}
#URL 딕셔너리로 하면 안에 있는지 확인 O(1)에 가능해서 리스트보다 성능에 좋음
url_dict = {
    '/api/haccp/pollingTest' : '폴링테스트',
    '/haccp/monitor' : 'HACCP모니터링',
    '/api/haccp/get_monitor' : 'HACCP모니터링',
    '/api/user/login' : '로그인',
    '/company/info' : '정보관리',
    '/product/dashboard' : '주문출하관리',
    '/product/shipment_list' : '주문출하관리',
    '/production/product_order_list' : '생산관리',
    '/document/haccp_doc_state' : 'HACCP모니터링',
    '/production/production_list' : '생산관리',
    '/haccp/kpi_list' : 'HACCP모니터링',
    '/api/haccp/detial_monitor' : 'HACCP모니터링',
    '/user/login' : '로그인',
    '/worker/list' : '정보관리',
    '/user/list' : '정보관리',
    '/standard/standard_list' : '정보관리',
    '/standard/sanitation_list' : '정보관리',
    '/standard/schedule_list' : '정보관리',
    '/material/list' : '구매관리',
    '/product/list' : '주문출하관리',
    '/company/list' : '정보관리',
    '/product/dashboard?product_kind=product' : '주문출하관리',
    '/product/dashboard?product_kind=oem' : '주문출하관리',
    '/material/dashboard' : '구매관리',
    '/document/haccp_doc_state?rows=10&page=1&start=&end=&search_list=subject%2C%60write%60&search=subject&keyword=' : 'HACCP모니터링',
    '/product/product_stock_list' : '주문출하관리',
    '/production/product_order_list?rows=10&page=1&start=&end=&search_list=order_group%2Corder_type%2Cproduct_name&search=ALL&keyword=&tab_column=order_type&tab=B' : '생산관리',
    '/production/product_order_list?rows=10&page=1&start=&end=&search_list=order_group%2Corder_type%2Cproduct_name&search=ALL&keyword=&tab_column=order_type&tab=C' : '생산관리',
    '/product/shipment_list?rows=10&page=1&start=&end=&search_list=release_state_text%2Cclient_name&search=ALL&keyword=&tab_column=order_type&tab=B' : '주문출하관리',
    '/product/shipment_list?rows=10&page=1&start=&end=&search_list=release_state_text%2Cclient_name&search=ALL&keyword=&tab_column=order_type&tab=C' : '주문출하관리',
    '/material/order_list' : '구매관리',
    '/material/warehouse_list' : '구매관리',
    '/material/warehouse_list?rows=10&page=1&start=&end=&search_list=material_name%2Ctask_type_text&search=ALL&keyword=&tab_column=material_kind&tab=maf' : '구매관리',
    '/material/warehouse_list?rows=10&page=1&start=&end=&search_list=material_name%2Ctask_type_text&search=ALL&keyword=&tab_column=material_kind&tab=raw' : '구매관리',
    '/material/warehouse_list?rows=10&page=1&start=&end=&search_list=material_name%2Ctask_type_text&search=ALL&keyword=&tab_column=material_kind&tab=sub' : '구매관리',
    '/production/production_run_list' : '생산관리',
    '/production/production_list?rows=10&page=1&start=&end=&search_list=product_name%2Cproduction_status_text&search=ALL&keyword=&tab_column=production_status&tab=W' : '생산관리',
    '/production/production_list?rows=10&page=1&start=&end=&search_list=product_name%2Cproduction_status_text&search=ALL&keyword=&tab_column=production_status&tab=C' : '생산관리',
    '/production/production_list?rows=10&page=1&start=&end=&search_list=product_name%2Cproduction_status_text&search=ALL&keyword=&tab_column=production_status&tab=D' : '생산관리',
    '/production/production_list?rows=10&page=1&start=&end=&search_list=product_name%2Cproduction_status_text&search=ALL&keyword=&tab_column=production_status&tab=all' : '생산관리',
    '/material/material_stock_list' : '구매관리',
    '/material/dashboard?material_kind=%EA%B0%80%EA%B3%B5%EC%9B%90%EB%A3%8C' : '구매관리',
    '/material/dashboard?material_kind=%EB%B6%80%EC%9E%90%EC%9E%AC' : '구매관리',
    '/material/list?rows=10&page=1&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=maf' : '구매관리',
    '/material/list?rows=10&page=1&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=raw' : '구매관리',
    '/material/list?rows=10&page=1&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=sub' : '구매관리',
    '/user/list?rows=10&page=2&search_list=name%2Cphone&search=name&keyword=' : '정보관리',
    '/user/list?rows=10&page=1&search_list=name%2Cphone&search=name&keyword=' : '정보관리',
    '/material/list?rows=10&page=1&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=oem' : '구매관리',
    '/material/list?rows=10&page=1&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=2&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=3&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=4&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=5&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=6&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/material/list?rows=10&page=8&start=&end=&search_list=material_code%2Cmaterial_name%2Ccompany_name&search=ALL&keyword=&tab_column=material_kind&tab=all' : '구매관리',
    '/company/list?rows=10&page=1&start=&end=&search_list=company_name%2Cbusiness_license_no%2Cmember_name%2Cmember_phone&search=ALL&keyword=&tab_column=company_kind&tab=MATERIAL' : '정보관리',
    '/company/list?rows=10&page=1&start=&end=&search_list=company_name%2Cbusiness_license_no%2Cmember_name%2Cmember_phone&search=ALL&keyword=&tab_column=company_kind&tab=CLIENT' : '정보관리',
    '/company/list?rows=10&page=1&start=&end=&search_list=company_name%2Cbusiness_license_no%2Cmember_name%2Cmember_phone&search=ALL&keyword=&tab_column=company_kind&tab=all' : '정보관리',
    '/production/product_order_list?rows=10&page=1&start=&end=&search_list=order_group%2Corder_type%2Cproduct_name&search=ALL&keyword=&tab_column=order_type&tab=all' : '생산관리',
    '/product/list?rows=10&page=1&start=&end=&search_list=product_kind_text%2Cproduct_name%2Cproduct_code&search=ALL&keyword=&tab_column=product_kind&tab=product' : '주문출하관리',
    '/product/list?rows=10&page=1&start=&end=&search_list=product_kind_text%2Cproduct_name%2Cproduct_code&search=ALL&keyword=&tab_column=product_kind&tab=oem' : '주문출하관리',
    '/product/list?rows=10&page=1&start=&end=&search_list=product_kind_text%2Cproduct_name%2Cproduct_code&search=ALL&keyword=&tab_column=product_kind&tab=all' : '주문출하관리',
    '/api/haccp/save_monitor' : 'HACCP모니터링',
    '/product/form?idx=26' : '주문출하관리',
    '/api/standard/detail_schedule' : '정보관리',
    '/haccp/monitor_warning' : 'HACCP모니터링',
    '/haccp/monitoring_log' : 'HACCP모니터링',
    '/api/company/save_company' : '정보관리',
    '/haccp/monitoring_log?rows=10&page=2&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=2&start=2021-08-11&end=2021-08-17&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=9&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=19&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=20&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=30&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=29&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=39&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=49&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=2&start=2021-08-01&end=2021-08-11&search_list=name%2Cstatus_text&search=ALL&keyword=%EB%83%89%EC%9E%A5%EC%B0%BD%EA%B3%A01' : 'HACCP모니터링',
    '/haccp/monitor_warning?rows=10&page=1&start=2021-08-01&end=2021-08-11&search_list=name%2Cstatus_text&search=ALL&keyword=%EB%83%89%EB%8F%99%EC%B0%BD%EA%B3%A0' : 'HACCP모니터링',
    '/haccp/monitor_warning?rows=10&page=1&start=2021-08-01&end=2021-08-11&search_list=name%2Cstatus_text&search=name&keyword=%EB%83%89%EB%8F%99%EC%B0%BD%EA%B3%A0' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=1&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=%EB%83%89%EB%8F%99%EC%B0%BD%EA%B3%A0' : 'HACCP모니터링',
    '/haccp/monitoring_log?rows=10&page=2&start=&end=&search_list=name%2Cstatus_text&search=ALL&keyword=%EB%83%89%EB%8F%99%EC%B0%BD%EA%B3%A0' : 'HACCP모니터링',
    '/api/haccp/detial_monitor_warning' : 'HACCP모니터링'
}


for file in file_list:
    with open('data/'+file, newline='') as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            #여기 조건 수정하세용
            if 'doraji' in row[8] and row[5]!='/' and '*' not in row[5] and '.css' not in row[5] and '.ico' not in row[5] and '.js' not in row[5] and '.png' not in row[5]:
                url_filtering_dict[row[5]] = "-"
                # print(row[5])

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

# key file 생성
makeKeyJSON()

# sql 쿼리문 생성
# writeSQL()