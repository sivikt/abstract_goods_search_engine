import logging
import logging.config
import os
import yaml
import urllib3

from pathlib import Path

from .config_default import get_arg


def setup():
    basedir = os.path.abspath(os.path.dirname(__file__))

    default_log_config_path = str(Path(basedir) / 'logging_default.yaml')

    log_config_path = get_arg('LOG_CONFIG', default=default_log_config_path)

    """Setup logging configuration
    """
    with open(str(log_config_path), 'rt') as f:
        log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

    logger = logging.getLogger(__name__)

    logger.info(f"Logging config {log_config_path}")

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
