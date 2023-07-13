import string
import random
import uuid
import re
import json
import base64
from . import config
from .constants import Path, Setting
from urllib.parse import urljoin, urlparse


def generate_uuid():
    return str(uuid.uuid4())


def generate_android_id():
    return f"android-{''.join(random.choices(string.hexdigits, k=16)).lower()}"


def shortcode_to_id(thread_url):
    """
    Reference : https://gist.github.com/sclark39/9daf13eea9c0b381667b61e3d2e7bc11?permalink_comment_id=2715416#gistcomment-2715416
    """
    if isinstance(thread_url, int) or thread_url.isnumeric():
        return thread_url
    thread_shortcode = urlparse(thread_url).path.split("/")[-1]
    code = ('A' * (12-len(thread_shortcode)))+thread_shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')


def generate_url(domain=None, url_path=None):
    if not domain and not url_path:
        raise
    if not domain:
        domain = Path.API_URL
    return urljoin(domain, url_path)


def generate_headers():
    Setting.DEVICE_ID = generate_uuid()
    Setting.ANDROID_ID = generate_android_id()
    # "Authorization": PUBLIC_TOKEN
    headers = {"Host": Path.HOST,
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "en-US",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "User-Agent": config.USER_AGENT,
               "X-Ig-Device-Id": Setting.DEVICE_ID,
               "X-Ig-Android-Id": Setting.ANDROID_ID,
               "X-Bloks-Version-Id": Setting.BLOK_VERSION_ID}
    return headers


def get_auth_token(response):
    token_data_regex = re.compile(r'''"{(.*?)}"''', re.VERBOSE)
    try:
        token_location = find_nested_key(
            response['layout']['bloks_payload']['tree'], "#")[0]
        token_data = token_data_regex.search(str(token_location)).group(0)
    except:
        raise Exception('Login Failed')
    while isinstance(token_data, str):
        token_data = json.loads(token_data)
    response_headers = json.loads(token_data['headers'])
    logged_in_user_data = json.loads(token_data['login_response'])[
        'logged_in_user']
    token = response_headers['IG-Set-Authorization']
    mid_token = str(response_headers.get('IG-Set-X-MID', None))
    user_id = str(response_headers.get('ig-set-ig-u-ds-user-id', None))
    headers = {"Authorization": token, "Ig-U-Ds-User-Id": user_id,
               "Ig-Intended-User-Id": user_id, "X-Mid": mid_token}
    config._DEFAULT_SESSION.headers.update(headers)
    return response_headers, logged_in_user_data


def find_nested_key(dataset=None, nested_key=None):
    def get_nested_data(dataset, nested_key, placeholder):
        if isinstance(dataset, list) or isinstance(dataset, dict) and dataset:
            if isinstance(dataset, list):
                for item in dataset:
                    get_nested_data(item, nested_key, placeholder)
            if isinstance(dataset, dict):
                if nested_key in dataset.keys():
                    placeholder.append(dataset.get(nested_key))
                for item in dataset.values():
                    get_nested_data(item, nested_key, placeholder)
        return placeholder
    return get_nested_data(dataset, nested_key, [])


def check_for_errors(response):
    if isinstance(response, dict):
        if "status" in response.keys():
            if response["status"] == "ok":
                return response
            if response["status"] != "ok":
                if "message" in response.keys():
                    print(response)
                    raise Exception(response['message'])
    return response


if __name__ == "__main__":
    pass
