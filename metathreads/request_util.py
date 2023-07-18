import httpx
import asyncio
import bs4
import json
import hashlib
from . import util
from . import config
from .constants import Path


def make_request(url=None, method=None, params=None, request_payload=None, session=None, timeout=None, **kwargs):
    global data_container
    # fmt: off - Turns off formatting for this block of code. Just for the readability purpose.
    def make_regular_request(request_payload):
        return validate_response(session.request(**request_payload))

    async def make_async_request(request_payload):
        pagination_data = request_payload.pop("pagination_data",None)
        if not pagination_data:
            response = await session.request(**request_payload)
            return validate_response(response)
        return await _handle_pagination(request_payload=request_payload,session=session,**{"end_cursor":pagination_data})

    async def make_concurrent_requests(request_payload):
        if isinstance(request_payload,list):
            tasks_list = [asyncio.create_task(make_async_request(payload)) for payload in request_payload]
        else:
            query_params = request_payload.pop("params",None)
            if not isinstance(query_params,list):
                return await make_async_request({"params":query_params} | request_payload) 
            if not query_params:
                return await make_async_request(request_payload)  
            tasks_list = [asyncio.create_task(make_async_request({"params":query} | request_payload)) for query in query_params]
        return await asyncio.gather(*tasks_list, return_exceptions=True)

    data_container = {}
    method = method or "GET"
    timeout = timeout or config.TIMEOUT or 10
    proxies = config.PROXY or None
    ssl_verify = False if proxies else True
    concurrent_requests = False
    session = session or config._DEFAULT_SESSION or httpx.Client(follow_redirects=True, timeout=timeout, proxies=proxies, verify=ssl_verify)
    if request_payload:
        concurrent_requests = True if isinstance(request_payload,list) or (isinstance(request_payload,dict) and isinstance(request_payload.get("params"),list) or request_payload.get("pagination_data")) else False
        if concurrent_requests:
            connection_limits = httpx.Limits(max_connections=100, max_keepalive_connections=10, keepalive_expiry=5)
            headers,cookies = session.headers,session.cookies
            session = httpx.AsyncClient(limits=connection_limits,headers=headers,cookies=cookies,follow_redirects=True,timeout=timeout,proxies=proxies,verify=ssl_verify)
            try:
                return asyncio.run(make_concurrent_requests(request_payload))
            except KeyboardInterrupt:
                print("Interuppted..")
                return list(data_container.values())
            except Exception as error:
                print(error)
                return list(data_container.values())
    else:
        request_payload = {"method":method,"url":url,"params":params} | kwargs
    return make_regular_request(request_payload)


def generate_request_data(endpoint, placeholder=None, params=None, additional_payload=None, pagination=None, return_payload=False, **kwargs):
        # fmt: off - Turns off formatting for this block of code. Just for the readability purpose.
    method = kwargs.pop("method",None) or "GET"
    params = params or {}
    url = kwargs.pop("url",None) or Path.API_URL
    url = util.generate_url(domain=url, url_path=endpoint)
    params,data,json_data = params,kwargs.pop("data",None),kwargs.pop("json",None)
    if additional_payload and isinstance(additional_payload,dict):
        existing_payload = params or data or json_data
        key,values = additional_payload.popitem()
        values = values[0] if isinstance(values,list) and len(values) == 1 else values
        if isinstance(values,list):
            additional_payload = [json.dumps(existing_payload | {key:str(each_item)}) if params else existing_payload | {key:str(each_item)} for each_item in values]
        else:
            additional_payload = json.dumps(existing_payload | {key:str(values)}) if params else existing_payload | {key:str(values)}
    else:
        additional_payload = json.dumps(params) if params else data or json_data if any([data,json_data]) else {}
    data_key = "params" if params else "data" if data else "json" if json_data else None
    additional_payload = {data_key:additional_payload} if data_key and additional_payload else {}
    if placeholder and isinstance(placeholder,list):
        request_payload = [{"method": method, "url": url.format(each_item)} | additional_payload | kwargs for each_item in placeholder]
    else:
        request_payload = {"method": method, "url": url.format(placeholder)} | additional_payload | kwargs
    # fmt: on   
    if data and "data" not in request_payload.keys():
        request_payload.update({"data": data})
    if return_payload:
        return request_payload
    if pagination:
        request_payload.update({"pagination_data": pagination}) if isinstance(request_payload, dict) else [
            item.update({"pagination_data": pagination}) for item in request_payload]
    return make_request(request_payload=request_payload)


async def _handle_pagination(url=None, request_payload=None, session=None, end_cursor=None, **kwargs):
        # fmt: off  - Turns off formatting for this block of code. Just for the readability purpose.
    unique_key = hashlib.sha1(json.dumps(request_payload, sort_keys=True).encode()).hexdigest()
    data_placeholder = {"data": [],"cursor_endpoint": None, "has_next_page": True}
    request_payload = request_payload or {"url": url} | kwargs
    cursor_key = next(iter(end_cursor))
    end_cursor = end_cursor[cursor_key]
    while data_placeholder["has_next_page"]:
        try:
            if end_cursor:
                query_params = request_payload["params"] or json.dumps({cursor_key:""})
                query_params = json.loads(query_params)
                query_params[cursor_key] = end_cursor
                request_payload["params"] = json.dumps(query_params)
            response = await session.request(**request_payload)
            response = validate_response(response)
            end_cursor = util.find_nested_key(response,"next_max_id") or util.find_nested_key(response,"paging_tokens")
            end_cursor = end_cursor[0] if (end_cursor and isinstance(end_cursor[0],str)) else end_cursor[0].get("downwards",None) if (end_cursor and isinstance(end_cursor[0],dict)) else None
            more_threads =  util.find_nested_key(response,"downwards_thread_will_continue")
            more_threads = more_threads[0] if more_threads else True
            data_placeholder['data'].append(response)
            data_container[unique_key] = data_placeholder
            print(f"Page: {len(data_placeholder['data'])}", end="\r")
            if end_cursor:
                data_placeholder['cursor_endpoint'] = end_cursor
            else:
                data_placeholder["has_next_page"] = False

            if not data_placeholder["has_next_page"] or not more_threads:
                return data_placeholder
        # fmt: on 
        except ConnectionError as error:
            print(error)
            continue

        except Exception as error:
            print(error)
            return data_placeholder


def validate_response(response):
    try:
        response_text = ""
        soup = bs4.BeautifulSoup(response.content, "lxml")
        if "json" in response.headers["Content-Type"]:
            return util.check_for_errors(response.json())
        response_text = "\n".join(
            [line.strip() for line in soup.text.split("\n") if line.strip()])
        response.raise_for_status()
        return soup
    except Exception as error:
        # print(f"{error}\n\n{response_text}\n")
        raise error


if __name__ == '__main__':
    pass
