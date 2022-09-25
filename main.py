from uu import Error
from crawler import Job104Spider
import yaml
import pandas as pd


with open('parameters.yaml', 'r') as f:
    parameters = yaml.safe_load(f)

filter_params = {
    'area': parameters['filter_params']['area'],  # (地區) 台北市
    # 's9': '1,2,4,8',  # (上班時段) 日班,夜班,大夜班,假日班
    # 's5': '0',  # 0:不需輪班 256:輪班
    # 'wktm': '1',  # (休假制度) 週休二日
    'isnew': parameters['filter_params']['isnew'],  # (更新日期) 0:本日最新 3:三日內 7:一週內 14:兩週內 30:一個月內
    # 'jobexp': '1,3,5,10,99',  # (經歷要求) 1年以下,1-3年,3-5年,5-10年,10年以上
    # 'newZone': '1,2,3,4,5',  # (科技園區) 竹科,中科,南科,內湖,南港
    # 'zone': '16',  # (公司類型) 16:上市上櫃 5:外商一般 4:外商資訊
    # 'wf': '1,2,3,4,5,6,7,8,9,10',  # (福利制度) 年終獎金,三節獎金,員工旅遊,分紅配股,設施福利,休假福利,津貼/補助,彈性上下班,健康檢查,團體保險
    # 'edu': '1,2,3,4,5,6',  # (學歷要求) 高中職以下,高中職,專科,大學,碩士,博士
    # 'remoteWork': '1',  # (上班型態) 1:完全遠端 2:部分遠端
    # 'excludeJobKeyword': '科技',  # 排除關鍵字
    # 'kwop': '1',  # 只搜尋職務名稱
}


max_mun = 50

job104_spider = Job104Spider()
jobs = job104_spider.search('data%20engineer%20數據工程師', max_mun, filter_params=filter_params)
jobs = [job104_spider.search_job_transform(job) for job in jobs]

result = pd.DataFrame()
for job in jobs:
    
    data = pd.DataFrame([job])
    result = result.append(data, ignore_index=False)
    result.sort_values(by=['job_id'])


existing_file = pd.read_excel('demo.xlsx', index_col=None)
existing_job = set(existing_file['job_id'])
new_job = list(result['job_id'])


for job_id in new_job:
    if job_id in existing_job:
        update_date = result.loc[result['job_id'] == job_id, 'appear_date'].values[0]
        existing_file.loc[existing_file['job_id'] == job_id, ['updated_date']] = update_date
    else:
        data = result.loc[result['job_id'] == job_id]
        existing_file = existing_file.append(data, ignore_index=False)

with pd.ExcelWriter('demo.xlsx', engine='xlsxwriter') as writer:
    existing_file.to_excel(writer, sheet_name='Sheet1', index=False, header= True)
    #result.to_excel(writer, sheet_name='Sheet1', index=False, header= True)



