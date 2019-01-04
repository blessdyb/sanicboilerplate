import aiohttp
from functools import wraps
from sanic.response import json
from .config import ASYNC_TIMEOUT


HTTP_RESPONSE_OK = 200
HTTP_RESPONSE_MULTI_STATUS = 207
HTTP_RESPONSE_BAD_REQUEST = 400
HTTP_RESPONSE_UNAUTHORIZED = 401
HTTP_RESPONSE_NOT_FOUND = 404
HTTP_RESPONSE_INTERNAL_SERVER_ERROR = 500
HTTP_RESPONSE_NOT_IMPLEMENTED = 501
HTTP_RESPONSE_BAD_GATEWAY = 502
HTTP_RESPONSE_TIMEOUT = 504

JSON_CONTENT_TYPE = 'application/json'


def validate_request():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if request.headers.get('content-type') == JSON_CONTENT_TYPE:
                try:
                    print('get request from ', request.path, ' with payload ', request.json)
                except Exception as e:
                    return json({
                        'data': {},
                        'errors':[{
                            'type': HTTP_RESPONSE_BAD_REQUEST,
                            'message': 'Your payload is not a valid JSON'
                        }]},
                        HTTP_RESPONSE_BAD_REQUEST)
            response = await f(request, *args, **kwargs)
            return response
        return decorated_function
    return decorator


async def requests(session, url, method, data):
    async with session.request(url=url, method=method, json=data) as response:
        if response.content_type == JSON_CONTENT_TYPE:
            response_data = await response.json()
        else:
            response_data = await response.text()
        return response.status, response_data


async def http_client(url, method='GET', data={}, headers={}):
    timeout = aiohttp.ClientTimeout(total=ASYNC_TIMEOUT)
    headers = {
        'content-type': JSON_CONTENT_TYPE,
        **headers
    }
    async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
        print('sending request to ', url)
        response = await requests(session, url, method, data)
        print('get response from ', url, response[0])
        return response
