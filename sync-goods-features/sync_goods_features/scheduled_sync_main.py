import logging
import threading

import config_logging
config_logging.setup()

from config import ARGS
from sync_goods_features import sync


logger = logging.getLogger(__name__)


def call_sync(**kwargs):
    try:
        sync(**kwargs)
    except Exception:
        logger.error('Error during synchronizing features', exc_info=True)


def sync_sleep_loop(sync_interval_seconds: int):
    ticker = threading.Event()

    call_sync(**ARGS)

    while not ticker.wait(sync_interval_seconds):
        call_sync(**ARGS)


if __name__ == '__main__':
    sync_sleep_loop(sync_interval_seconds=ARGS['sync_interval_seconds'])
