import json
from optparse import OptionParser

from elasticsearch import Elasticsearch


def setup_search_templates(es_client: Elasticsearch, template_id: str):
    def map_keys_to_json_str(src_map):
        return ',\n'.join([f'"{k}": {json.dumps(v)}' for k, v in src_map.items()])

    """ Statuses ordered by importance. More important statuses have lower number and must have higher relevance score.
    1 - famous
    2 - famous abandoned
    3 - live
    4 - live abandoned
    5 - dead
    6 - dead abandoned
    
    The idea is to boost scores according to the status importance but at the same time put exact matches to the top.
    Also match by MaterialSerialNumber as a first priority. We expect only few matches in this case. 
    """

    search_query = {
        "bool": {
            "should": [
                {"script_score":
                    {"query":
                        {"match": {
                            "MaterialSerialNumber": {
                                "query": "{{q}}",
                                "_name": "serial_number_match"
                            }
                        }
                        },
                        "script": {
                            "source": "256*_score"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.raw_normalized": {
                                "query": "{{q}}",
                                "_name": "full_match_1"
                            }
                        }
                        },
                        "script": {
                            "source": "128*_score*Math.exp(Math.log(0.9)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.raw_normalized_concat": {
                                "query": "{{q}}",
                                "_name": "full_match_2"
                            }
                        }
                        },
                        "script": {
                            "source": "128*_score*Math.exp(Math.log(0.9)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.stemmed_words": {
                                "query": "{{q}}",
                                "operator": "AND",
                                "_name": "full_match_3"
                            }
                        }
                        },
                        "script": {
                            "source": "128*_score*Math.exp(Math.log(0.9)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.1_7shingles": {
                                "query": "{{q}}",
                                "_name": "shingles_match"
                            }
                        }
                        },
                        "script": {
                            "source": "64*_score*Math.exp(Math.log(0.6)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.4grams": {
                                "query": "{{q}}",
                                "minimum_should_match": "80%",
                                "_name": "4grams_match"
                            }
                        }
                        },
                        "script": {
                            "source": "16*_score*Math.exp(Math.log(0.4)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                },

                {"script_score":
                    {"query":
                        {"match": {
                            "GoodsId.3grams": {
                                "query": "{{q}}",
                                "minimum_should_match": "70%",
                                "_name": "3grams_match"
                            }
                        }
                        },
                        "script": {
                            "source": "_score*Math.exp(Math.log(0.2)*(doc['GoodsStatusId'].value-1))"
                        }
                    }
                }
            ]
        }
    }

    search_query_with_scoring = {
        "query": search_query,
        "stored_fields": ["_source", "matched_queries"],
        "sort": {
            "_script": {
                "type": "number",
                "script": {
                    "lang": "painless",
                    "source": """
                        // double score_norm = doc['GoodsLiveMinMaxNorm'].value + doc['ClassesFract'].value;                
                        return _score;
                    """
                },
                "order": "desc"
            }
        }
    }

    es_client.put_script(id=template_id, body={
        'script': {
            'lang': 'mustache',
            'source': f'{{ {map_keys_to_json_str(search_query_with_scoring)},' + \
                      '"_source": {{#tojson}}fields{{/tojson}},' + \
                      '"track_scores": true,' + \
                      '"track_total_hits": true,' + \
                      '"from": {{from}}{{^from}}0{{/from}},' + \
                      '"size": {{size}}{{^size}}10{{/size}}}'
        }
    }, timeout='1m')


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-h', '--elastic_host', dest='elastic_host', default='localhost:9200',
                      help='ElasticSearch hostname')
    parser.add_option('-u', '--elastic_user', dest='elastic_user', help='ElasticSearch username')
    parser.add_option('-p', '--elastic_pass', dest='elastic_pass', help='ElasticSearch password')
    parser.add_option('-t', '--template_id', dest='template_id', help='Index search template ID')

    (options, args) = parser.parse_args()

    if not options.template_id:
        parser.error('template_id is required')

    if options.elastic_user:
        elastic_credentials = (options.elastic_user, options.elastic_pass)
    else:
        elastic_credentials = None

    es = Elasticsearch(
        hosts=[options.elastic_host],
        http_auth=elastic_credentials
    )

    setup_search_templates(es, options.template_id)
