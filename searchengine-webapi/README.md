# Search engine REST API Specification

## 1. Purpose

This application serves as a REST API web service and answers free search form requests to find Goods.

## 2. General notes

Application is written in Python >= 3.8 using Flask web framework.  
There is also one-page React based Web UI application
located at [searchengine-webui](searchengine-webui) which can be used for convenience in demo purposes. Although this 
application is outdated and should be repaired and deployed into [searchengine_webapi ui](searchengine_webapi/static).

## 3. Configuration
Sample configuration is in [searchengine_webapi config](searchengine_webapi/config/config_default.py).

> Note that all properties are expected to be set via environment variables. So, to configure the application first 
> set up its configuration properties as system environment variables.

| Property                                          | Meaning                                                                                                                                         |
|:--------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------|
| OAUTH2_SERVICE_URI                                |  OAUTH service endpoint which is used to validate authentication JWT tokens. Default value is *https://auth-goods-dev.azurewebsites.net*  |
| OAUTH2_JWKS_URI                                   |  URI of keys store. Default value is ***OAUTH2_SERVICE_URI**/.well-known/openid-configuration/jwks*                                             |
| OAUTH2_JWT_ISSUER_CLAIM                           |  Expected JWT issuer. Default value is *https://auth-goods-dev.azurewebsites.net*                                                         |
| OAUTH2_JWT_AUDIENCE_CLAIM                         |  Expected JWT audience. Default value is *goods_api*                                                                                      |
| ELASTICS_ENDPOINT                                 |  ElasticSearch hostname or IP address in format <host&vert;IP:port>                                                                             |
| ELASTICS_USERNAME                                 |  ElasticSearch username to access *ELASTIC_HOST*                                                                                                |
| ELASTICS_PASSWORD                                 |  ElasticSearch password to access *ELASTIC_HOST*                                                                                                |
| ELASTICS_USE_SSL                                  |  The flag indicating if we should use SSL to access ElasticSearch or not                                                                        |
| ELASTICS_TARGET_INDEX_ALIAS                       |  Destination ElasticSearch index to read Documents from. Can be either index name or index alias                                                |
| ELASTICS_GOODS_FREE_SEARCH_DEFAULT_PAGE_SIZE |  Number of found most relevant items to return per page                                                                                         |
| ELASTICS_GOODS_FREE_SEARCH_TEMPLATE_ID       |  Search query template ID which is use to request Documents from ElasticSearch                                                                  |


## 4. Deployment

> Read [uWSGI documentation](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html) to possibly tune WSGI based
application.
   
To develop/deploy locally prepare virtual environment and run `sh run-locally.sh` or `python wsgi.py`.  
To run in Azure Web App see [azure-webapp](deployment/azure-webapp/README.md).
