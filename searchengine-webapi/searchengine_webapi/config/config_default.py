import os


def get_arg(name: str, required: bool = False, default=None):
    full_name = f'SEARCHENGINE_WEBAPI_{name}'
    val = os.getenv(full_name, default)

    if val is None and required:
        raise Exception(f'Argument {full_name} is required')

    return val


APP_CONFIG_PATH = get_arg('APP_CONFIG_PATH')


class Config(object):
    OAUTH2_SERVICE_URI \
        = get_arg('OAUTH2_SERVICE_URI', default='https://auth-goods-dev.azurewebsites.net')

    OAUTH2_JWKS_URI \
        = get_arg('OAUTH2_JWKS_URI', default=f'{OAUTH2_SERVICE_URI}/.well-known/openid-configuration/jwks')

    OAUTH2_JWT_ISSUER_CLAIM \
        = get_arg('OAUTH2_JWT_ISSUER_CLAIM', default='https://auth-goods-dev.azurewebsites.net')

    OAUTH2_JWT_AUDIENCE_CLAIM \
        = get_arg('OAUTH2_JWT_AUDIENCE_CLAIM', default='goods_api')

    ELASTICS_ENDPOINT \
        = get_arg('ELASTICS_ENDPOINT', default='localhost:9200')

    ELASTICS_USERNAME \
        = get_arg('ELASTICS_USERNAME')

    ELASTICS_PASSWORD \
        = get_arg('ELASTICS_PASSWORD')

    ELASTICS_USE_SSL \
        = get_arg('ELASTICS_USE_SSL', default='false').lower() == 'true'

    ELASTICS_TARGET_INDEX_ALIAS \
        = get_arg('ELASTICS_TARGET_INDEX_ALIAS', default='goods_features_index')

    ELASTICS_GOODS_FREE_SEARCH_DEFAULT_PAGE_SIZE \
        = int(get_arg('ELASTICS_GOODS_FREE_SEARCH_DEFAULT_PAGE_SIZE', default=25))

    ELASTICS_GOODS_FREE_SEARCH_TEMPLATE_ID \
        = get_arg('ELASTICS_GOODS_FREE_SEARCH_TEMPLATE_ID', default='goods_free_search')
