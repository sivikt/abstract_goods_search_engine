from . import __version__

from flask import Blueprint
# from flask import current_app

main_pages_bp = Blueprint('main_pages', __name__)


# @main_pages_bp.route('/')
# def root():
#     return current_app.send_static_file('index.html')


@main_pages_bp.route('/version', methods=['GET'])
def version():
    return __version__
