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


    def search_job_transform(self, job_data):
        company_addr = f"{job_data['jobAddrNoDesc']} {job_data['jobAddress']}"
        job_url = f"https:{job_data['link']['job']}"
        job_id = job_url.split('/job/')[-1]

        if '?' in job_id:
            job_id = job_id.split('?')[0]

        job = {
            'job_id': job_id,
            'job_title': job_data['jobName'],
            'company_name': job_data['custName'],
            'company_addr': company_addr,
            'job_url': job_url,
            'period': job_data['periodDesc'],
            'appear_date': job_data['appearDate'], 
            'updated_date': None,
        }
        return job


    
    
    
    
   
    
    

    
    

    