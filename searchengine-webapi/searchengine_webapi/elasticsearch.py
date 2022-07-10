import logging

import elasticsearch as es_driver

logger = logging.getLogger(__name__)


class ElasticSearch:
    def __init__(self):
        self._app = None
        self._cli = None

    def init_app(self, app):
        self._app = app
        self.connect()

    def connect(self):
        if self._app.config['ELASTICS_USERNAME']:
            elastic_credentials = (self._app.config['ELASTICS_USERNAME'], self._app.config['ELASTICS_PASSWORD'])
        else:
            elastic_credentials = None

        self._cli = es_driver.Elasticsearch(
            hosts=[self._app.config['ELASTICS_ENDPOINT']],
            http_auth=elastic_credentials,
        )

        return self._cli

    def get_db(self):
        if not self._cli:
            return self.connect()
        return self._cli


es_client = ElasticSearch()
