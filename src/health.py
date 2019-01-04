from sanic.response import json
from sanic.blueprints import Blueprint
from src import config
from src.utils import HTTP_RESPONSE_OK


health_blueprint = Blueprint('health', url_prefix='/__STATUS__')

@health_blueprint.get('/health')
async def status_info(request):
    info = {
        'debug': config.DEBUG,
        'env': config.PYTHON_ENV,
        'version': config.VERSION,
    }
    return json(info, HTTP_RESPONSE_OK)
