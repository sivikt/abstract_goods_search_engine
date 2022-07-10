import datetime
from optparse import OptionParser

from elasticsearch import Elasticsearch


def setup_index(es_client: Elasticsearch):
    index_settings = {
      "settings": {
        "max_ngram_diff": 4,
        "max_shingle_diff": 6,

        "analysis": {
          "normalizer": {
            "gds_name_raw_normalizer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols",
                "remove_same_consecutive_letters_cfilter"
              ],
              "filter": [
                "lowercase",
                "asciifolding",
                "elision"
              ]
            },
            "gds_name_raw_normalizer_concat": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols",
                "remove_same_consecutive_letters_cfilter",
                "remove_spaces"
              ],
              "filter": [
                "lowercase",
                "asciifolding",
                "elision"
              ]
            }
          },
          "analyzer": {

            "gds_name_stemmed_words_analyzer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols"
              ],
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "asciifolding",
                "apostrophe",
                "elision",
                "remove_same_consecutive_letters",
                "gds_stemmer"
              ]
            },

            "gds_name_stemmed_1_7shingles_words_analyzer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols"
              ],
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "asciifolding",
                "apostrophe",
                "elision",
                "remove_same_consecutive_letters",
                "gds_stemmer",
                "1_7_words_joiner"
              ]
            },

            "gds_name_stemmed_words_metaphone_analyzer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols"
              ],
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "asciifolding",
                "apostrophe",
                "elision",
                "remove_same_consecutive_letters",
                "gds_stemmer",
                "gds_metaphone"
              ]
            },

            "gds_name_3gram_analyzer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols",
                "kill_dot_apostrophe_symbols",
                "remove_same_consecutive_letters_cfilter",
                "remove_spaces"
              ],
              "tokenizer": "gds_3gram_tokenizer",
              "filter": [
                "lowercase",
                "asciifolding",
                "apostrophe",
              ]
            },

            "gds_name_4gram_analyzer": {
              "type": "custom",
              "char_filter": [
                "percent_symbol_to_word",
                "plus_symbol_to_word",
                "equal_symbol_to_word",
                "logical_symbol_conjunction",
                "logical_symbol_disjunction",
                "special_symbols_synonyms",
                "underscore_symbol_to_space",
                "big_gaps_to_single_space",
                "replace_special_symbols_with_gap",
                "kill_unknown_symbols",
                "kill_dot_apostrophe_symbols",
                "remove_same_consecutive_letters_cfilter",
                "remove_spaces"
              ],
              "tokenizer": "gds_4gram_tokenizer",
              "filter": [
                "lowercase",
                "asciifolding",
                "apostrophe",
              ]
            }
          },
          "tokenizer": {
              "gds_3gram_tokenizer": {
                  "type": "ngram",
                  "min_gram": 3,
                  "max_gram": 3
               },
               "gds_4gram_tokenizer": {
                  "type": "ngram",
                  "min_gram": 4,
                  "max_gram": 4
               }
          },
          "filter": {
            "gds_metaphone": {
                "type": "phonetic",
                "encoder": "double_metaphone",
                "max_code_len": 400,
                "replace": "true"
            },
            "gds_stemmer": {
              "type": "stemmer",
              "language": "english"
            },
            "1_7_words_joiner": {
                 "type": "shingle",
                 "max_shingle_size": 7,
                 "min_shingle_size": 2,
                 "output_unigrams": "true",
                 "token_separator": ""
             },
            "remove_same_consecutive_letters": {
              "type": "pattern_replace",
              "pattern": "([a-zA-Z])\\1+",
              "replacement": "$1$1"
            }
          },
          "char_filter": {
            "special_symbols_synonyms": {
              "type": "mapping",
              "mappings": [
                "$  => _dollar_",
                "€  => _euro_",
                "￡ => _pound_",
                "￥ => _yuan_yen_",
                "#  => _number_hashtag_"
              ]
            },
            "underscore_symbol_to_space": {
              "type": "pattern_replace",
              "pattern": "_+",
              "replacement": " "
            },
            "remove_spaces": {
              "type": "pattern_replace",
              "pattern": " +",
              "replacement": ""
            },
            "percent_symbol_to_word": {
              "type": "pattern_replace",
              "pattern": "%+",
              "replacement": " percent "
            },
            "plus_symbol_to_word": {
              "type": "pattern_replace",
              "pattern": "\\++",
              "replacement": " plus and add "
            },
            "equal_symbol_to_word": {
              "type": "pattern_replace",
              "pattern": "=+",
              "replacement": " equal "
            },
            "big_gaps_to_single_space": {
              "type": "pattern_replace",
              "pattern": "(\\s)+",
              "replacement": " "
            },
            "logical_symbol_conjunction": {
              "type": "pattern_replace",
              "pattern": "&+",
              "replacement": " and amp ampersand "
            },
            "logical_symbol_disjunction": {
              "type": "pattern_replace",
              "pattern": "\\|+",
              "replacement": " or pipe vertical bar stick line "
            },
            "replace_special_symbols_with_gap": {
                "type": "pattern_replace",
                "pattern": "[\"|~|`|(|)|<|>|{|}|?|!|\\^|:|;|/|\\\\|*|«|»]",
                "replacement": " ",
                "all": "false"
            },
            "remove_same_consecutive_letters_cfilter": {
              "type": "pattern_replace",
              "pattern": "([a-zA-Z])\\1+",
              "replacement": "$1$1"
            },
            "kill_unknown_symbols": {
                "type": "pattern_replace",
                "pattern": "[.+&&[^ \\p{L}]]",
                "replacement": "",
                "all": "false"
            },
            "kill_dot_apostrophe_symbols": {
                "type": "pattern_replace",
                "pattern": "[\.|']",
                "replacement": "",
                "all": "false"
            }
          }
        },

        "similarity": {
            "stemmed_words_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            },

            "metaphone_stemmed_words_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            },

            "3grams_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            },

            "4grams_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            },

            "1_7shingles_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0

            },

            "raw_normalized_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            },

            "raw_normalized_concat_similarity": {
                "type" : "BM25",
                #"b": 0.5,
                #"k1": 0
            }
        }
      },

      "mappings": {
        "properties": {
          "MaterialSerialNumber": {
            "type": "keyword",
            "index": "true"
          },
          "UpdateDate": {
             "type": "date",
             "format": "strict_date_optional_time_nanos",
             "index": "false"
          },
          "UpdateNum": {
             "type": "long",
             "index": "false"
          },
          "GoodandService": {
            "type": "text",
            "index": "true"
          },
          "OwnerName": {
            "type": "text",
            "index": "false"
          },
          "OwnerAddress": {
            "type": "text",
            "index": "false"
          },
          "GoodsProducer": {
            "type": "text",
            "index": "false"
          },
          "Classes": {
            "type": "text",
            "index": "false"
          },
          "GoodsStatusClass": {
            "type": "text",
            "index": "false"
          },
          "GoodsStatusClassInt": {
            "type": "integer",
            "index": "false"
          },
          "GoodsStatusId": {
            "type": "byte",
            "index": "false"
          },
          "StatusCode": {
            "type": "text",
            "index": "false"
          },
          "StatusDesc": {
            "type": "text",
            "index": "false"
          },
          "StatusDate": {
            "type": "date",
            "format": "strict_date_optional_time_nanos",
            "index": "false"
          },
          "GoodsDeliveryDate": {
            "type": "date",
            "format": "strict_date_optional_time_nanos",
            "index": "false"
          },
          "PrimaryCode": {
            "type": "text",
            "index": "false"
          },
          "TypeID": {
            "type": "text",
            "index": "false"
          },
          "ListOrder": {
            "type": "text",
            "index": "false"
          },
          "GoodsRefsCount": {
            "type": "long",
            "index": "false"
          },
          "GoodsDeadCount": {
            "type": "long",
            "index": "false"
          },
          "GoodsLiveMinMaxNorm": {
            "type": "float",
            "index": "false"
          },
          "GoodsDeadMinMaxNorm": {
            "type": "float",
            "index": "false"
          },
          "ClassesFract": {
            "type": "float",
            "index": "false"
          },
          "GoodsId": {
            "type": "keyword",
            "index": "true",
            "store": "true",
            "fields": {
                "stemmed_words": {
                    "type": "text",
                    "index": "true",
                    "term_vector": "with_positions",
                    "analyzer": "gds_name_stemmed_words_analyzer",
                    "search_analyzer": "gds_name_stemmed_words_analyzer",
                    "norms": "true",
                    "store": "true",
                    "fielddata": "false",
                    "similarity" : "stemmed_words_similarity"
                },
                "metaphone_stemmed_words": {
                    "type": "text",
                    "index": "true",
                    "term_vector": "with_positions",
                    "analyzer": "gds_name_stemmed_words_metaphone_analyzer",
                    "search_analyzer": "gds_name_stemmed_words_metaphone_analyzer",
                    "norms": "true",
                    "store": "true",
                    "fielddata": "false",
                    "similarity" : "metaphone_stemmed_words_similarity"
                },
                "3grams": {
                    "type": "text",
                    "index": "true",
                    "term_vector": "yes",
                    "analyzer": "gds_name_3gram_analyzer",
                    "search_analyzer": "gds_name_3gram_analyzer",
                    "norms": "true",
                    "store": "true",
                    "fielddata": "false",
                    "similarity" : "3grams_similarity"
                },
                "4grams": {
                    "type": "text",
                    "index": "true",
                    "term_vector": "yes",
                    "analyzer": "gds_name_4gram_analyzer",
                    "search_analyzer": "gds_name_4gram_analyzer",
                    "norms": "true",
                    "store": "true",
                    "fielddata": "false",
                    "similarity" : "4grams_similarity"
                },
                "1_7shingles": {
                    "type": "text",
                    "index": "true",
                    "term_vector": "yes",
                    "analyzer": "gds_name_stemmed_1_7shingles_words_analyzer",
                    "search_analyzer": "gds_name_stemmed_1_7shingles_words_analyzer",
                    "norms": "true",
                    "store": "true",
                    "fielddata": "false",
                    "similarity" : "1_7shingles_similarity"
                },
                "raw_normalized": {
                  "type": "keyword",
                  "index": "true",
                  "normalizer": "gds_name_raw_normalizer",
                  "norms": "true",
                  "store": "true",
                  "similarity" : "raw_normalized_similarity"
                },
                "raw_normalized_concat": {
                  "type": "keyword",
                  "index": "true",
                  "normalizer": "gds_name_raw_normalizer_concat",
                  "norms": "true",
                  "store": "true",
                  "similarity" : "raw_normalized_concat_similarity"
                }
            }
          },
          "GoodsIdExpansion": {
              "type": "keyword",
              "index": "true",
              "store": "true",
              "fields": {
                  "stemmed_words": {
                      "type": "text",
                      "index": "true",
                      "term_vector": "with_positions",
                      "analyzer": "gds_name_stemmed_words_analyzer",
                      "search_analyzer": "gds_name_stemmed_words_analyzer",
                      "norms": "true",
                      "store": "true",
                      "fielddata": "false",
                      "similarity": "stemmed_words_similarity"
                  },
                  "raw_normalized": {
                      "type": "keyword",
                      "index": "true",
                      "normalizer": "gds_name_raw_normalizer",
                      "norms": "true",
                      "store": "true",
                      "similarity": "raw_normalized_similarity"
                  },
                  "raw_normalized_concat": {
                      "type": "keyword",
                      "index": "true",
                      "normalizer": "gds_name_raw_normalizer_concat",
                      "norms": "true",
                      "store": "true",
                      "similarity": "raw_normalized_concat_similarity"
                  }
              }
          }
        }
      }
    }

    index_name = f"gds_names_index_{datetime.datetime.today().strftime('%Y%m%d_%H%M%S')}"

    es_client.indices.create(index=index_name, body=index_settings)

    return index_name


if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] arguments')
    parser.add_option('-h', '--elastic_host', dest='elastic_host', default='localhost:9200', help='ElasticSearch hostname')
    parser.add_option('-u', '--elastic_user', dest='elastic_user', help='ElasticSearch username')
    parser.add_option('-p', '--elastic_pass', dest='elastic_pass', help='ElasticSearch password')

    (options, args) = parser.parse_args()

    if options.elastic_user:
        elastic_credentials = (options.elastic_user, options.elastic_pass)
    else:
        elastic_credentials = None

    es = Elasticsearch(
        hosts=[options.elastic_host],
        http_auth=elastic_credentials
    )

    target_index = setup_index(es_client=es)

    print('created index name', target_index)
