import pandas as pd


class Processor:
    def __init__(self, job_keywords):
        self.job_keywords = job_keywords
    
    def process_data(self, existed_data, new_data):
        for job in new_data:
            current_job = pd.DataFrame([job])
            if not self.is_related_job(current_job):
                continue

            is_existed_job = self.check_job_exists(current_job, existed_data)

            if is_existed_job:
                self.renew_updated_date(current_job, existed_data)
            else:
                existed_data = self.add_new_job(current_job, existed_data)
        return existed_data

    def is_related_job(self, current_job: pd.DataFrame):
        current_job_title = current_job['job_title'].values[0]
        for keyword in self.job_keywords:
            if keyword.lower() in current_job_title.lower():
                return False
        
        return True

    def check_job_exists(self, current_job: pd.DataFrame, existed_data: pd.DataFrame):
        current_job_id = current_job['job_id'].values[0]
        existed_jobs_id = set(existed_data['job_id'])

        if current_job_id in existed_jobs_id:
            return True
        else:
            return False

    def renew_updated_date(self, current_job: pd.DataFrame, existed_data: pd.DataFrame):
        current_job_id = current_job['job_id'].values[0]
        update_date = current_job.loc[current_job['job_id'] == current_job_id, 'appear_date'].values[0]
        existed_data.loc[existed_data['job_id'] == current_job_id, ['updated_date']] = update_date

    def add_new_job(self, current_job: pd.DataFrame, existed_data: pd.DataFrame):
        existed_data = pd.concat([existed_data, current_job], ignore_index=True)
        return existed_data