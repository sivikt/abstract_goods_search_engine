import os
from configparser import ConfigParser


def get_arg(name: str, required: bool = False, default=None):
    full_name = f'SYNC_GOODS_FEATURES_{name}'
    val = os.getenv(full_name, default)

    if val is None and required:
        raise Exception(f'Argument {full_name} is required')

    return val


if get_arg('CONFIG_FILE'):
    cfg = ConfigParser()
    cfg.read(get_arg('CONFIG_FILE'))
    for k,v in dict(cfg.items('default')).items():
        os.environ[f'SYNC_GOODS_FEATURES_{k.upper()}'] = v

ARGS = dict(
    mssql_source_table=get_arg('MSSQL_SOURCE_TABLE', default='ES_GoodsApplication'),
    mssql_username=get_arg('MSSQL_USERNAME', required=True),
    mssql_password=get_arg('MSSQL_PASSWORD', required=True),
    mssql_host=get_arg('MSSQL_HOST', default='localhost'),
    mssql_schema=get_arg('MSSQL_SCHEMA', required=True),
    mssql_read_batch_size=int(get_arg('MSSQL_READ_BATCH_SIZE', default='500000')),
    elastic_host=get_arg('ELASTIC_HOST', default='localhost:9200'),
    elastic_write_batch_size=int(get_arg('WRITE_BATCH_SIZE', default='500000')),
    elastic_username=get_arg('ELASTIC_USERNAME'),
    elastic_password=get_arg('ELASTIC_PASSWORD'),
    elastic_target_index=get_arg('ELASTIC_TARGET_INDEX', required=True),
    sync_interval_seconds=int(get_arg('SYNC_INTERVAL_SECONDS', default=str(2*60)))
)
