FROM python:3.7

ARG APP_VERSION
ARG API_MODULE_CFG

ENV APP_HOME=/tm-search-app
ENV API_MODULE=searchengine_webapi
ENV DEPLOYMENT_HOME=deployment/docker-uwsgi
ENV API_MODULE_LOG_CFG=logging_dev.yaml
ENV UWSGI_CFG=uwsgi.ini
ENV APP_PORT=8080

ENV searchengine_webapi_app_version=$APP_VERSION
ENV searchengine_webapi_app_config=$APP_HOME/$API_MODULE/config/config.yaml
ENV searchengine_webapi_log_config=$APP_HOME/$API_MODULE/config/config_log.yaml

COPY $API_MODULE $APP_HOME/$API_MODULE
COPY requirements.txt $APP_HOME
COPY $DEPLOYMENT_HOME/$UWSGI_CFG $APP_HOME
COPY $API_MODULE_CFG $searchengine_webapi_app_config
COPY $DEPLOYMENT_HOME/$API_MODULE_LOG_CFG $searchengine_webapi_log_config
COPY $DEPLOYMENT_HOME/start.sh $APP_HOME

RUN apt-get update && \
    apt-get install -y python3-dev build-essential

WORKDIR $APP_HOME

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install uwsgi

EXPOSE $APP_PORT

RUN chmod +x ./start.sh

CMD ["./start.sh"]