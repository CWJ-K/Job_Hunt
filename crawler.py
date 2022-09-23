import time
import random
import requests

import time
import random
import requests


class Job104Spider():

    def search(self, keyword, max_mun=10, filter_params=None, sort_type='符合度', is_sort_asc=False):
        jobs = []
        total_count = 0

        url = 'https://www.104.com.tw/jobs/search/list'
        query = f'ro=0&kwop=7&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
        if filter_params:
            query += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://www.104.com.tw/jobs/search/',
        }

        # 加上排序條件
        sort_dict = {
            '符合度': '1',
            '日期': '2',
            '經歷': '3',
            '學歷': '4',
            '應徵人數': '7',
            '待遇': '13',
        }
        sort_params = f"&order={sort_dict.get(sort_type, '1')}"
        sort_params += '&asc=1' if is_sort_asc else '&asc=0'
        query += sort_params

        page = 1
        while len(jobs) < max_mun:
            params = f'{query}&page={page}'
            r = requests.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('請求失敗', r.status_code)
                data = r.json()
                print(data['status'], data['statusMsg'], data['errorMsg'])
                break

            data = r.json()
            total_count = data['data']['totalCount']
            jobs.extend(data['data']['list'])

            if (page == data['data']['totalPage']) or (data['data']['totalPage'] == 0):
                break
            page += 1
            time.sleep(random.uniform(3, 5))

        return jobs[:max_mun]

    def get_job(self, job_id):
        """取得職缺詳細資料"""
        url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': f'https://www.104.com.tw/job/{job_id}'
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            return

        data = r.json()
        return data['data']

    def search_job_transform(self, job_data):
        """將職缺資料轉換格式、補齊資料"""
        apply_num = int(job_data['applyCnt'])
        company_addr = f"{job_data['jobAddrNoDesc']} {job_data['jobAddress']}"

        job_url = f"https:{job_data['link']['job']}"
        job_company_url = f"https:{job_data['link']['cust']}"
        job_analyze_url = f"https:{job_data['link']['applyAnalyze']}"

        job_id = job_url.split('/job/')[-1]
        if '?' in job_id:
            job_id = job_id.split('?')[0]

        salary_high = int(job_data['salaryLow'])
        salary_low = int(job_data['salaryHigh'])

        job = {
            'job_id': job_id,
            #'type': job_data['jobType'],
            'name': job_data['jobName'],  # 職缺名稱
            # 'desc': job_data['descSnippet'],  # 描述
            'appear_date': job_data['appearDate'],  # 更新日期
            #'apply_num': apply_num,
            #'apply_text': job_data['applyDesc'],  # 應徵人數描述
            'company_name': job_data['custName'],  # 公司名稱
            'company_addr': company_addr,  # 工作地址
            'job_url': job_url,  # 職缺網頁
            #'job_analyze_url': job_analyze_url,  # 應徵分析網頁
            #'job_company_url': job_company_url,  # 公司介紹網頁
            #'lon': job_data['lon'],  # 經度
            #'lat': job_data['lat'],  # 緯度
            #'education': job_data['optionEdu'],  # 學歷
            'period': job_data['periodDesc'],  # 經驗年份
            #'salary': job_data['salaryDesc'],  # 薪資描述
            #'salary_high': salary_high,  # 薪資最高
            #'salary_low': salary_low,  # 薪資最低
            'tags': job_data['tags'],  # 標籤
        }
        return job


    
    
    
    
   
    
    

    
    

    