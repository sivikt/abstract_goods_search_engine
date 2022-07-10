#!/bin/bash

if [ -n "$1" ]; then
  version=$1
else
  version="SNAPSHOT-0.0.1"
fi

if [ -n "$2" ]; then
  app_cfg=$2
else
  app_cfg="delivery/tm-search-app/searchengine_webapi/config/config_local.yaml"
fi

#python3 -c "import nltk; nltk.download('punkt', download_dir='./sync_goods_features/nltk_data/')"

echo "Build version $version"
echo "App config $app_cfg"

export SERVICE_NAME=searchengine_webapi
export SERVICE_VER=$version

docker build . -f deployment/docker-uwsgi/Dockerfile --build-arg API_MODULE_CFG="$app_cfg" --build-arg APP_VERSION="$version" -t $SERVICE_NAME
