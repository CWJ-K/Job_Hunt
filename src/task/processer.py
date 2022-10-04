import pandas as pd


def process_data(existed_data, new_data):
    for job in new_data:
        current_job = pd.DataFrame([job])
        if not is_related_job(current_job):
            continue

        is_existed_job = check_job_exists(current_job, existed_data)

        if is_existed_job:
            renew_updated_date(current_job, existed_data)
        else:
            existed_data = add_new_job(current_job, existed_data)
    return existed_data


def is_related_job(current_job: pd.DataFrame):
    keywords = [
        '前端', '後端', '系統', 'Quality', '品質', '電源', '客服',
        '臨床', '主管', '機構', 'Golang', 'Unity', 'HW', 'Server',
        '派遣', 'Hardware', 'Stack', 'FW', 'ASIC', 'iOS', 'QA', 'Android',
        'Electrical', '5G', 'Design', '副理', '實習生', 'Wind', 'EDI', '約聘',
        '資深', 'Application ', 'MEMS', '運維', '韌體', '測試', 'SW', 'Java', 'Senior',
        '機械', 'IC', 'Hardware', 'Test', '製程', 'Manager', 'PCB', 'Wireless', 'Internship', 'Game', 'Testing'
        ]

    current_job_title = current_job['job_title'].values[0]
    for keyword in keywords:
        if keyword.lower() in current_job_title.lower():
            return False
    
    return True


def check_job_exists(current_job: pd.DataFrame, existed_data: pd.DataFrame):
    current_job_id = current_job['job_id'].values[0]
    existed_jobs_id = set(existed_data['job_id'])

    if current_job_id in existed_jobs_id:
        return True
    else:
        return False


def renew_updated_date(current_job: pd.DataFrame, existed_data: pd.DataFrame):
    current_job_id = current_job['job_id'].values[0]
    update_date = current_job.loc[current_job['job_id'] == current_job_id, 'appear_date'].values[0]
    existed_data.loc[existed_data['job_id'] == current_job_id, ['updated_date']] = update_date


def add_new_job(current_job: pd.DataFrame, existed_data: pd.DataFrame):
    existed_data = pd.concat([existed_data, current_job], ignore_index=True)
    return existed_data