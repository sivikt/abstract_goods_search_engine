import logging
import json

from flask import Response
from flask import request


logger = logging.getLogger(__name__)


class RequestParameterMissedException(Exception):
    """Raised when the request parameter is expected but was not passed"""
    pass


class RequestParameterMeaningException(Exception):
    """Raised when the request parameter has an unknown meaning"""
    pass


def get_request_query_parameter(name, param_type=None, default=None, required: bool = False):
    try:
        rv = request.args[name]
    except KeyError:
        if required:
            raise RequestParameterMissedException(f"Parameter {name} is required")
        else:
            return default

    if param_type is not None and rv is not None:
        try:
            rv = param_type(rv)
        except ValueError:
            raise RequestParameterMeaningException(f"Parameter '{name}' has incorrect meaning")

    return rv


def create_api_error(error_code: str = 'unknown', error_desc: str = 'unknown'):
    return {
        'error_code': error_code,
        'error_desc': error_desc
    }


def json_response(r: Response) -> Response:
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    return r


def response_error_404(error_code: str, error_desc: str) -> Response:
    return json_response(Response(json.dumps(create_api_error(error_code, error_desc)), status=404))


def response_error_400(error_code: str, error_desc: str) -> Response:
    return json_response(Response(json.dumps(create_api_error(error_code, error_desc)), status=400))


def response_error_401(error_descr: str = 'bad credentials') -> Response:
    return json_response(Response(json.dumps(create_api_error('unauthorized', error_descr)), status=401))


def response_error_500(error_code: str, error_desc: str) -> Response:
    return json_response(Response(json.dumps(create_api_error(error_code, error_desc)), status=500))


def response_200(data) -> Response:
    return json_response(Response(json.dumps(data), status=200))
