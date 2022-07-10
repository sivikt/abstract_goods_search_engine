import logging.config
import os
import yaml

from pathlib import Path


def setup():
    basedir = os.path.abspath(os.path.dirname(__file__))

    default_log_config_path = str(Path(basedir) / 'logging_default.yaml')

    with open(str(default_log_config_path), 'rt') as f:
        log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
