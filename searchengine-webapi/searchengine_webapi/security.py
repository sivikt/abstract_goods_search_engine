import logging

import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWKError, InvalidTokenError

from functools import wraps

from flask import request
from flask import current_app

from .responses_util import response_error_401

from requests.exceptions import HTTPError


logger = logging.getLogger(__name__)


def jwt_auth():
    def _jwt_auth(f):
        @wraps(f)
        def __jwt_auth(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            auth_prefix = 'Bearer '

            if auth_header.startswith(auth_prefix):
                try:
                    jwt_token = auth_header[len(auth_prefix):].strip()
                    authorize(jwt_access_token=jwt_token)
                except HTTPError:
                    logger.error('ISE during authentication/authorization', exc_info=True)
                    return response_error_401()
                except InvalidTokenError:
                    logger.error('ISE during authentication/authorization', exc_info=True)
                    return response_error_401(error_descr='invalid jwt token')
                except PyJWKError:
                    logger.error('ISE during authentication/authorization', exc_info=True)
                    return response_error_401(error_descr='invalid jwt token')

                return f(*args, **kwargs)
            else:
                return response_error_401(error_descr='only bearer token authorization is supported')

        return __jwt_auth

    return _jwt_auth


def authorize(jwt_access_token: str = None) -> dict:
    jwks_client = PyJWKClient(current_app.config['OAUTH2_JWKS_URI'])
    signing_key = jwks_client.get_signing_key_from_jwt(jwt_access_token)

    return jwt.decode(
        jwt_access_token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=current_app.config['OAUTH2_JWT_ISSUER_CLAIM'],
        audience=current_app.config['OAUTH2_JWT_AUDIENCE_CLAIM']
    )
