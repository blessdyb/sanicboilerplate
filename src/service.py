from asyncio import get_event_loop, gather
from .utils import HTTP_RESPONSE_OK


async def bulk_async_wrapper(request, data, processor):
    event_loop = get_event_loop()
    async_tasks =[event_loop.create_task(processor(request, item)) for item in data]
    async_responses = await gather(*async_tasks)
    return async_responses


async def bulk_http_requests_from_third_party(request, data=[]):
    async_responses = await bulk_async_wrapper(request, data, http_request_from_third_party)
    return async_responses


async def http_request_from_third_party(request, data={}):
    status_code, response = await request.app.http_client('https://beendless.com')
    if status_code == HTTP_RESPONSE_OK:
        return response
    else:
        return {'success': False}
