import pytest
import pandas as pd
import yaml
from pathlib import Path
import os
from ...src.task.processer import Processor


PARENT_PATH = Path(__file__).resolve().parents[2]

YAML_PATH = os.path.join(PARENT_PATH, 'src', 'parameters.yaml')

with open(YAML_PATH, 'r', encoding='utf-8') as f:
    parameters = yaml.load(f, Loader=yaml.FullLoader)

data_processor = Processor(parameters['job_keywords'])


@pytest.mark.parametrize(
    ('current_job', 'existed_job', 'boolean'),
    [   
        (pd.DataFrame({'job_id': ['7gore']}), pd.DataFrame({'job_id': ['7gore', '9ajdi']}), True,),
        (pd.DataFrame({'job_id': ['8owie']}), pd.DataFrame({'job_id': ['7gore', '9ajdi']}), False,),
        (pd.DataFrame({'job_id': ['5wiej']}), pd.DataFrame({'job_id': []}), False,),
        ]
    )
def test_check_job_exists(current_job, existed_job, boolean):
    pytest.assume(data_processor.check_job_exists(current_job, existed_job) == boolean)


@pytest.mark.parametrize(
    ('current_job', 'existed_data', 'expected_result', 'boolean'),
    [   
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220920'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220920'], 'updated_date': ['20220925']}),
            True,
            ),
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['20220925']}),
            True,
            ),
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            False
            ),

        ]
    )
def test_renew_updated_date(current_job, existed_data, expected_result, boolean):
    data_processor.renew_updated_date(current_job, existed_data)

    pytest.assume(existed_data.equals(expected_result) == boolean)



@pytest.mark.parametrize(
    ('current_job', 'existed_data', 'expected_result'),
    [   
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['8owie'], 'appear_date': ['20220920'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['8owie', '7gore'], 'appear_date': ['20220920', '20220925'], 'updated_date': ['', '']})
            ),
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['8owie', '9ajdi'], 'appear_date': ['20220921', '20220922'], 'updated_date': ['20220925', '20220925']}),
            pd.DataFrame({'job_id': ['8owie', '9ajdi', '7gore'], 'appear_date': ['20220921', '20220922', '20220925'], 'updated_date': ['20220925', '20220925', '']})
            ),
        ]
    )
def test_add_new_job(current_job, existed_data, expected_result):
    existed_data = data_processor.add_new_job(current_job, existed_data)
    pytest.assume(existed_data.equals(expected_result))


@pytest.mark.parametrize(
    ('current_job', 'expected_result'),
    [
        (pd.DataFrame({'job_title': ['前端工程師']}), False),
        (pd.DataFrame({'job_title': ['QA工程師']}), False),
        (pd.DataFrame({'job_title': ['Data Front-end Engineer']}), False),
        ]
    )
def test_is_related_job(current_job, expected_result):
    assert data_processor.is_related_job(current_job)==expected_result
