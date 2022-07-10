# Goods features synchronization Specification

## 1. Purpose

This application gets Goods data (features) from MSSQL database table 
and puts it into ElasticSearch.

## 2. General notes

Only one synchronizer must be run.  
No support for distributed synchronization.

Data source table on MSSQL must be updated fully in a transaction so the 
synchronizer won't read intermediate results. 

## 3. Configuration
Sample configuration file is **local_config.ini**.

| Property                 | Meaning                                                                              |
|--------------------------|:------------------------------------------------------------------------------------:|
| SYNC_INTERVAL_SECONDS    |  An integer representing a period in seconds after which next synchronization occurs |
| MSSQL_SOURCE_TABLE       |  Source table name in MSSQL from which application will get Goods data          |
| MSSQL_SCHEMA             |  Source MSSQL schema name where *MSSQL_SOURCE_TABLE* is located                      |
| MSSQL_USERNAME           |  MSSQL username to access *MSSQL_SOURCE_TABLE*                                       |
| MSSQL_PASSWORD           |  MSSQL password to access *MSSQL_PASSWORD*                                           |
| MSSQL_HOST               |  MSSQL hostname or IP address                                                        |
| MSSQL_READ_BATCH_SIZE    |  Number of records to read from *MSSQL_SOURCE_TABLE* at once                         |
| ELASTIC_HOST             |  ElasticSearch hostname or IP address in format <host&vert;IP:port>                  |
| ELASTIC_USERNAME         |  ElasticSearch username to access *ELASTIC_HOST*                                     |
| ELASTIC_PASSWORD         |  ElasticSearch password to access *ELASTIC_HOST*                                     |
| ELASTIC_TARGET_INDEX     |  Destination ElasticSearch index to write Goods data to                         |
| ELASTIC_WRITE_BATCH_SIZE |  Number of records to write into *ELASTIC_TARGET_INDEX* at once                      |


## 4. Deployment

> At the MSSQL side one has to enable SNAPSHOT transaction isolation level.

### 4.1 Docker
1. `docker build . -f deployment/docker/Dockerfile -t sync-goods-features`  
   Got **<image_id>**.
2. Copy properties from the file **local_config.ini** into **<config_name>.env** file.
   Change application properties as environment variables inside **<config_name>.env** 
   according your dev/staging/prod environment. Set batch sizes to fit into the host memory.  
   Got **<config_name>.env**.
3. `docker run --env-file **<config_name>.env** **<image_id>**`.  
   Got **<container_id>**.
4. `docker logs -f **<container_id>** &> **<log_name>.log** &`