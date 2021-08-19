import pandas as pd

info_management = {
    "urls": [
        "/company/company_info",
        "/company/worker_list",
        "/company/member_list",
        '/standard/haccp_standard_list',
        '/standard/sanitation_standard_list',
        '/standard/haccp_document_list',
        '/haccp/monitor_limit',
        '/materials/materials_maf_list',
        '/materials/materials_raw_list',
        '/materials/materials_sub_list',
        '/product/product_list',
        '/product/mixing_ratios',
        '/materials/materials_oem_list',
        '/materials/company_list',
        '/client/client_list',
        '/security/security_list'
    ],
    "title": '정보관리'
}

purchase_management = {
    "urls": [
        '/materials/stock_dashboard_main',
        '/materials/stock_dashboard_sub',
        '/materials/stock_dashboard_oem',
        '/materials/order_list',
        '/materials/warehouse_list',
        '/materials/stock_list'
    ],
    'title': '구매관리'
}

order_processing = {
    'urls': [
        '/client/receive_an_order_list',
        '/client/b2c_order_list',
        '/client/urgency_order_list'
    ],
    'title': '주문관리'
}

production_management = {
    'urls': [
        '/production/today_production_list',
        '/production/today_materials_list',
        '/production/preprocess_list',
        '/production/cook_list',
        '/production/wrapping_list'
    ],
    'title': '생산관리'
}

shipment_management = {
    'urls': [
        '/client/shipment_list',
        '/client/packing_dashboard'
    ],
    'title': '출하관리'
}

HACCP_monitoring = {
    'urls': [
        '/doc/doc_state',
        '/haccp/monitor',
        '/haccp/monitor_warning_list',
        '/haccp/monitoring_log',
        '/production/production_record_list',
        '/doc/doc_state',
        '/haccp/kpi_list',
        '/client/sales_promotion_list'
    ],
    'title': 'HACCP모니터링'
}

data_management = {
    'urls': [
        '/client/sales_promotion_list',
        '/client/sales_list',
    ],
    'title': '자료관리'
}

measurement = {
    'urls': [
        '/api/receive_temperature'
    ],
    'title': '측정'
}
login = {
    'urls': [
        '/auth/login',
        '/user/login'
    ],
    'title': '로그인'
}

category_list = [info_management, purchase_management, order_processing, production_management,
                 shipment_management, HACCP_monitoring, data_management, measurement, login]

useless_urls = [
    "/aqua/views/v01/public", '/favicon',
]

df = pd.read_csv('./csv_output_file.csv')

newdf = []


def isUseless(target):  # uselsee_urls 안에 있는거랑 / * 제외
    if target == '/' or target == "*":
        return True
    for useless in useless_urls:
        if useless in target:
            return True
    return False


def classifyCategory(target):  # category_list 안에 있는거랑 비교// 모르는 url은 '-' 로..
    for category in category_list:
        for url in category['urls']:
            if url in target:
                return category['title']
    return '-'


for idx in range(0, df.shape[0]):  # main
    if(isUseless(df.iloc[idx]['URL'])):  # 필요없는 URL 걸러주고
        continue
    result = classifyCategory(df.iloc[idx]['URL'])  # 비교해서 category(사용구분) 알랴줌
    temp = {
        '로그일시': df.iloc[idx]['Date Time'],
        '사용구분': result,
        '사용자': df.iloc[idx]['Log Name'],
        '접속IP': df.iloc[idx]['Host'],
        '데이터 크기': df.iloc[idx]['Bytes Sent'],
        'URL': df.iloc[idx]['URL'],
        'Method': df.iloc[idx]['Method']
    }
    newdf.append(temp)

file_df = pd.DataFrame(newdf)


file_df.to_csv('./result.csv', encoding='utf-8-sig', index=None)
