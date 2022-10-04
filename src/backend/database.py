import pandas as pd
from sqlalchemy import engine
from loguru import logger
from backend.clients import get_mysql_connection

CONNECTION = get_mysql_connection()

def read_data_from_mysql():
    data = pd.read_sql('SELECT * FROM jobs', con=CONNECTION)
    return data


def update_data_to_mysql_by_pandas(
    data: pd.DataFrame,
    table: str,
    mysql_connection: engine.base.Connection = CONNECTION,
):
    if len(data) > 0:
        try:
            data.to_sql(
                name=table,
                con=mysql_connection,
                if_exists='replace',
                index=False,
                chunksize=1000,
            )
        except Exception as e:
            logger.info(e)
            return False

    #CONNECTION.close()
    return True