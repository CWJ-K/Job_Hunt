import os
from uu import Error
import yaml
import pandas as pd

from task.crawler import Job104Spider
from task.processer import process_data
from backend.database import read_data_from_mysql, update_data_to_mysql_by_pandas


CURRENT_DIR = os.path.dirname(__file__)
YAML_PATH = os.path.join(CURRENT_DIR, 'parameters.yaml')

with open(YAML_PATH, 'r', encoding='utf-8') as f:
    parameters = yaml.load(f, Loader=yaml.FullLoader)


filter_params = {
    'area': parameters['filter_params']['area'],
    'isnew': parameters['filter_params']['isnew'],  
    #'jobexp': parameters['filter_params']['jobexp'],
    'excludeJobKeyword': parameters['filter_params']['excludeJobKeyword'],
    'kwop': parameters['filter_params']['kwop'],
}

max_mun = 300

job104_spider = Job104Spider()
jobs = job104_spider.search('data%20engineer%20數據工程師', max_mun, filter_params=filter_params)
new_data = [job104_spider.search_job_transform(job) for job in jobs]


existed_data = read_data_from_mysql()

final_data = process_data(existed_data, new_data)

update_data_to_mysql_by_pandas(final_data, 'jobs')



