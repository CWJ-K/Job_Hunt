import pytest
import pandas as pd

from ...src.task.processer import check_job_exists, renew_updated_date, add_new_job

@pytest.mark.parametrize(
    ('current_job', 'existed_job'),
    [   
        (pd.DataFrame({'job_id': ['7gore']}), pd.DataFrame({'job_id': ['7gore', '9ajdi']})),
        (pd.DataFrame({'job_id': ['8owie']}), pd.DataFrame({'job_id': ['7gore', '9ajdi']})),
        (pd.DataFrame({'job_id': ['5wiej']}), pd.DataFrame({'job_id': []})),
        (pd.DataFrame({'job_id': []}), pd.DataFrame({'job_id': []})),
        ]
    )
def test_check_job_exists(current_job, existed_job):
    pytest.assume(check_job_exists(current_job, existed_job))


@pytest.mark.parametrize(
    ('current_job', 'existed_data', 'expected_result'),
    [   
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220920'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220920'], 'updated_date': ['20220925']})
            ),
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['20220925']})
            ),
        (
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']}),
            pd.DataFrame({'job_id': ['7gore'], 'appear_date': ['20220925'], 'updated_date': ['']})
            ),

        ]
    )
def test_renew_updated_date(current_job, existed_data, expected_result):
    renew_updated_date(current_job, existed_data)

    pytest.assume(existed_data.equals(expected_result))



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
    existed_data = add_new_job(current_job, existed_data)
    pytest.assume(existed_data.equals(expected_result))