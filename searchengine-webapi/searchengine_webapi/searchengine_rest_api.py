import logging

from typing import List

from flask import Blueprint
from flask import current_app

from .elasticsearch import es_client
from .responses_util import (
    response_200,
    response_error_400,
    get_request_query_parameter,
    RequestParameterMeaningException
)
from .security import jwt_auth


searchengine_rest_api_bp = Blueprint('searchengine_rest_api', __name__)


logger = logging.getLogger(__name__)


def do_search(answer_fields: List[str], add_meta: bool = False):
    try:
        search_query = get_request_query_parameter('q', required=True)

        items_per_query = get_request_query_parameter(
            'size',
            default=current_app.config['ELASTICS_GOODS_FREE_SEARCH_DEFAULT_PAGE_SIZE'],
            param_type=int
        )

        start_query_from = get_request_query_parameter('from', default=0, param_type=int)
    except RequestParameterMeaningException as ex:
        return response_error_400('illegal_param_meaning', str(ex))

    target_index = current_app.config['ELASTICS_TARGET_INDEX_ALIAS']

    if not search_query:
        return response_200({})

    raw_results = es_client.get_db().search_template(
        index=target_index,
        body={
            "id": current_app.config['ELASTICS_GOODS_FREE_SEARCH_TEMPLATE_ID'],
            "params": {
                "q": search_query,
                "size": items_per_query,
                "from": start_query_from,
                "fields": answer_fields
            }
        },
        request_timeout=120
    )

    answer = {
        'total_matched': raw_results['hits']['total']['value']
    }

    # if there is an exact match by id = MaterialSerialNumber limit the number of results to return to 1
    if len(raw_results['hits']['hits']) > 0 and raw_results['hits']['hits'][0]['_id'] == search_query:
        answer['total_matched'] = 1

    if add_meta:
        answer['findings'] = [
            {
                **res['_source'],
                'meta': {'_score': res['_score'], '_sort': res.get('sort', [-1])[0]}
            }
            for res in raw_results['hits']['hits'][:answer['total_matched']]
        ]
    else:
        answer['findings'] = [
            {
                **res['_source']
            }
            for res in raw_results['hits']['hits'][:answer['total_matched']]
        ]

    return response_200(answer)


@searchengine_rest_api_bp.route('/search_extended', methods=['GET'])
@jwt_auth()
def search_extended():
    return do_search(
        answer_fields=["MaterialSerialNumber", "GoodsId", "GoodandService",
                       "GoodsStatusClass", "GoodsRefsCount", "GoodsDeadCount",
                       "OwnerName", "OwnerAddress", "GoodsProducer", "StatusDesc"],
        add_meta=True
    )


@searchengine_rest_api_bp.route('/search', methods=['GET'])
@jwt_auth()
def search():
    return do_search(
        answer_fields=["MaterialSerialNumber", "GoodsId", "GoodandService",
                       "GoodsStatusId", "GoodsStatusClass", "OwnerName", "OwnerAddress", "GoodsProducer",
                       "StatusCode", "StatusDesc", "StatusDate", "GoodsDeliveryDate", "TypeID", "ListOrder",
                       "PrimaryCode", "StatusCode", "PartyName"]
    )
