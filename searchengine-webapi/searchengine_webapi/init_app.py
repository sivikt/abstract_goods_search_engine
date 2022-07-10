from .config import config_logging
from .config.config_default import Config
from .config.config_default import APP_CONFIG_PATH

import logging
from flask import Flask

from .elasticsearch import es_client
from .error_handling import init_error_handlers
from .main_pages import main_pages_bp
from .searchengine_rest_api import searchengine_rest_api_bp


logger = logging.getLogger(__name__)


def init_app():
    config_logging.setup()

    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    if APP_CONFIG_PATH:
        app.config.from_pyfile(APP_CONFIG_PATH, silent=False)
        logger.info(f"Loaded app config from {APP_CONFIG_PATH}")

    #logger.debug(f"FULL APP CONFIG {app.config}")

    with app.app_context():
        es_client.init_app(app)

        app.register_blueprint(main_pages_bp)
        app.register_blueprint(searchengine_rest_api_bp)

        init_error_handlers(app)

        return app
