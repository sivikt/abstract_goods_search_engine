# Specification

## 1. Purpose
This module is for Index setup. It includes index configuration and structure, and search query templates.

## 2. Initial Index setup
### 2.1 Environment

1. Install Python >= 3.7
2. `pip install -r requirements.txt`

### 2.2 Index structure
To create an index from scratch execute  
> python setup_index.py -h <elastic_search_host> -u <elastic_username> -p <elastic_password>

It returns the name of the index, `<gds_index_name>`, which has just been created.

Then one can deploy and run [sync-goods-features](sync-goods-features/README.md) having 
`<gds_index_name>` as a parameter.

### 2.3 Alias Index
In order to abstract of a specific index put an alias to your newly created index:

```python
es_client.indices.update_aliases(body={
   "actions": [
     { "add":    { "index": "<gds_index_name>", "alias": "<gds_index_alias>" }},
   ]
})
```

### 2.4 Search templates setup
ElasticSearch search query template defines what to search and how to search. The templates
are used by Search Engine.
To create a search templates for a particular index, e.g. `<gds_index_name>`, execute  
> python setup_search_templates.py -h <elastic_search_host> -u <elastic_username> -p <elastic_password> -t <search_template_id>

Then one can deploy and run [searchengine-webapi](searchengine-webapi/README.md) having 
`<gds_index_name>` (or `<gds_index_alias>`) and `<search_template_id>` as parameters.

## 3. How to update an existing Index

If there is an already existing Index which operates in production and one wants to make some 
changes in it then one can follow the next steps:

0. Develop new index structure and/or search approach.
1. Create a new index according to [2.1](#2.2-index-structure), get created index name `<gds_names_index_NEW>`.
2. Create a new search template if needed according to to [2.4](#2.4-search-templates-setup), get created template 
   id `<search_template_id_NEW>`.
3. Change the config of [sync-goods-features](sync-goods-features) application to point to a new index 
   `<gds_names_index_NEW>`. Or deploy a new version of the application with updated configuration.
4. Restart the application and wait until it finishes the execution.
5. Check the new index and new search templates to be sure it works as expected. E.g. automatically or manually 
   run integration tests to check correctness and quality metrics. If something wrong then go to step 0.
6. Change the alias to point to the new index `<gds_names_index_NEW>` and rewrite the old template with the new one 
   having the old template ID unchanged  

```python
es_client.indices.update_aliases(body={
   "actions": [
     { "remove": { "index": "<gds_names_index>", "alias": "<gds_index_alias>" }},
     { "add":    { "index": "<gds_names_index_NEW>", "alias": "<gds_index_alias>" }},
   ]
})

python setup_search_templates.py -h <elastic_search_host> -u <elastic_username> -p <elastic_password> -t <search_template_id>
```
> Note it may cause some disruptions in current live Users sessions. To avoid it and do the migration smoothly you can
> deploy a new version of [searchengine-webapi](searchengine-webapi) having `<gds_names_index_NEW>` and 
> `<search_template_id_NEW>` as parameters. And then redirect all traffic to that new version and decommission the old one.  

8. If everything works as expected, then remove/close the old index `<gds_names_index>`, remove old `<search_template_id>`
   and decommission the old versions of applications. Otherwise, remove the new index `<gds_names_index_NEW>`, 
   new search template `<search_template_id_NEW>`, new version of the applications, created in the steps 3 and 6,
   and go to 0.
