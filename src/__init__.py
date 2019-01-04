import src.config as config
from markdown2 import Markdown
from asyncio import get_event_loop
from sanic import Sanic, response
from sanic.blueprints import Blueprint
from .health import health_blueprint
from .utils import http_client
from .service import http_request_from_third_party, bulk_http_requests_from_third_party


app = Sanic(__name__)
app.config.from_object(config)


@app.listener('before_server_start')
async def set_up_http_client(app, loop):
    app.http_client = http_client


@app.get('/')
async def index(request):
    event_loop = get_event_loop()
    file = await event_loop.run_in_executor(None, open, './README.md')
    markdowner = Markdown()
    data = await event_loop.run_in_executor(None, file.read)
    return response.html(markdowner.convert(data))

@app.get('/sample')
async def sample(request):
    data = await http_request_from_third_party(request)
    return response.text(data)


@app.get('/samples')
async def samples(request):
    data = await bulk_http_requests_from_third_party(request, [1,2])
    return response.text(data)


@app.get('/docs')
def handle_request(request):
    return response.redirect('/docs/index.html')

docs_blueprint = Blueprint('docs', url_prefix='/docs')
docs_blueprint.static('/', './docs')

app.blueprint(docs_blueprint)
app.blueprint(health_blueprint)
