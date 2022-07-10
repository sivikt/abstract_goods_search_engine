import logging

from .responses_util import response_error_500, response_error_404, response_error_400


logger = logging.getLogger(__name__)


def handle_400(e):
    return response_error_400('bad_request', 'Bad Request')


def handle_404(e):
    return response_error_404('not_found', 'Requested resource not found')


def handle_ise(e):
    logger.error('ISE occurred', exc_info=e)
    return response_error_500('ise', 'Something went wrong. Contact an administrator')


def init_error_handlers(app):
    app.register_error_handler(400, handle_400)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_ise)
