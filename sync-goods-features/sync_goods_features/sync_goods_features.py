import logging
import pandas as pd
import numpy as np
import time
from functools import wraps
from typing import Iterator, Optional

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import sqlalchemy as sal


logger = logging.getLogger(__name__)

logger.info('pandas=%s', pd.__version__)
logger.info('numpy=%s', np.__version__)
logger.info('sqlalchemy=%s', sal.__version__)


def timeit(func):
    @wraps(func)
    def decorator(*arg, **kwargs):
        t = time.time()
        res = func(*arg, **kwargs)
        logger.info("%s took %s secs", func.__name__, round(time.time() - t, 1))
        return res

    return decorator


def connect_to_mssql_db(host: str, username: str, password: str, schema: str):
    connection_uri = sal.engine.url.URL.create(
        'mssql+pyodbc',
        username=username,
        password=password,
        host=host,
        database=schema,
        query={'driver': 'ODBC Driver 17 for SQL Server'},
    )

    engine = sal.create_engine(connection_uri, fast_executemany=True)

    return engine.connect()


# def from_mssql_datetime_str(dt_str: str) -> dt.datetime:
#     return dt.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
#
#
# def to_mssql_datetime_str(dt_tm: dt.datetime) -> str:
#     return dt_tm.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
#
#
# def inc_datetime_in_mssql_resolution(dt_tm: dt.datetime) -> dt.datetime:
#     return dt_tm + dt.timedelta(milliseconds=1)


def get_max_update_version_in_index(es_client: Elasticsearch, index_name: str) -> Optional[int]:
    resp = es_client.search(
        body={
            'query': {'match_all': {}},
            'size': 0,
            'aggs': {
                'update_version_stats': {'max': {'field': 'UpdateNum'}}
            }
        },
        index=index_name
    )

    max_update_version = resp['aggregations']['update_version_stats'].get('value', None)
    logger.info('Max documents Update Version = "%s"', max_update_version)

    return max_update_version


def get_data(db_connection,
             data_source_table: str,
             start_from: int = None,
             batch_size: int = None
             ) -> Iterator[pd.DataFrame]:
    if start_from:
        logger.info('selecting rows equal or bigger then "%s"', start_from)

        query = f"SELECT * FROM {data_source_table} WHERE UpdateNum >= {start_from} ORDER BY UpdateNum ASC"
    else:
        logger.info('selecting all rows from scratch')

        query = f"SELECT * FROM {data_source_table} ORDER BY UpdateNum ASC"

    db_connection = db_connection.execution_options(
        isolation_level="SNAPSHOT"
    )

    data_cursor = pd.read_sql(
        query,
        db_connection,
        chunksize=batch_size
    )

    iter_start_at = time.time()

    for chunk_df in data_cursor:
        iter_stop_at = time.time()
        diff_secs = iter_stop_at - iter_start_at

        yield chunk_df, round(diff_secs, 1)

        iter_start_at = time.time()


@timeit
def index_dataframe(es_client: Elasticsearch, index_name: str, df: pd.DataFrame, batch_size: int = None):
    def docs_generator():
        for i, company_info in df.iterrows():
            company_info = company_info.to_dict()

            yield {
                '_index': index_name,
                '_id': company_info['MaterialSerialNumber'],
                '_source': company_info
            }

    bulk(
        client=es_client,
        actions=docs_generator(),
        chunk_size=batch_size,
        timeout='20m',
        request_timeout=1200,
        raise_on_error=True,
        raise_on_exception=True
    )


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[~df.GoodsId.isnull() & (df.GoodsId != '')]
    df = df.replace({'GoodandService': np.nan}, '')
    df = df.replace({'OwnerName': np.nan}, '')
    df = df.replace({'OwnerAddress': np.nan}, '')
    df = df.replace({'GoodsProducer': np.nan}, '')
    df = df.replace({'Classes': np.nan}, '')
    df = df.replace({'ClassesFract': np.nan}, 0)

    return df


@timeit
def index_all_dataframes(es_client: Elasticsearch,
                         data_iterator: Iterator[pd.DataFrame],
                         index_name: str,
                         index_batch_size: int = None):
    total_indexed = 0

    for i, (input_batch, read_time_secs) in enumerate(data_iterator):
        good_data = preprocess_data(input_batch)

        logger.info('input_batch_no=%s read_time_secs=%s input_batch_size=%s selected_for_indexing=%s',
                    i, read_time_secs, len(input_batch), len(good_data))

        index_dataframe(es_client=es_client, index_name=index_name, df=good_data, batch_size=index_batch_size)

        total_indexed += len(good_data)

    logger.info('total_indexed=%s', total_indexed)


def get_new_data_and_index(mssql_connection,
                           mssql_source_table: str,
                           mssql_read_batch_size: int,
                           es_client: Elasticsearch,
                           es_index_name: str,
                           es_write_batch_size
                           ):

    marker = f'{es_index_name}_is_in_update_status'

    marker_exists_apriori = es_client.indices.exists_alias(name=marker, index=es_index_name)

    max_update_version = get_max_update_version_in_index(es_client=es_client, index_name=es_index_name)

    '''If marker exists it means previous update failed for some reasons.
    If it did then we need to read the data starting exactly from max_update_date
    to read what we had not read before failure.
    Otherwise, update was successful and we had read all new rows by that time, so now
    we are going to read more new rows which, we assume, must have update date bigger
    then our current max_update_date.
    '''
    if not marker_exists_apriori and max_update_version:
        max_update_version += 1

        logger.info('signal that synchronization has been started by adding alias %s', marker)

        es_client.indices.update_aliases(body={
            "actions": [
                {"add": {"index": es_index_name, "alias": marker}}
            ]
        })
    else:
        logger.info('alias %s has already been added', marker)

    data_gen = get_data(
        db_connection=mssql_connection,
        data_source_table=mssql_source_table,
        start_from=max_update_version,
        batch_size=mssql_read_batch_size
    )

    index_all_dataframes(
        es_client=es_client,
        data_iterator=data_gen,
        index_name=es_index_name,
        index_batch_size=es_write_batch_size
    )

    es_client.indices.update_aliases(body={
        "actions": [
            { "remove": { "index": es_index_name, "alias": marker }}
        ]
    })


@timeit
def sync(**kwargs):
    if kwargs['elastic_username']:
        elastic_credentials = (kwargs['elastic_username'], kwargs['elastic_password'])
    else:
        elastic_credentials = None

    es = Elasticsearch(
        hosts=[kwargs['elastic_host']],
        http_auth=elastic_credentials,
        http_compress=True
    )

    db_conn = connect_to_mssql_db(
        host=kwargs['mssql_host'],
        username=kwargs['mssql_username'],
        password=kwargs['mssql_password'],
        schema=kwargs['mssql_schema']
    ).execution_options(
        stream_results=True
    )

    get_new_data_and_index(mssql_connection=db_conn,
                           mssql_source_table=kwargs['mssql_source_table'],
                           mssql_read_batch_size=kwargs['mssql_read_batch_size'],
                           es_client=es,
                           es_index_name=kwargs['elastic_target_index'],
                           es_write_batch_size=kwargs['elastic_write_batch_size'])
