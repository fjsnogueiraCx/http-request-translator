from __future__ import print_function

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

from .url import get_url, check_valid_url
from .templates import php_template


def generate_script(headers, details, search_string=None):
    """Generate the php script corresponding to the passed request.

    :param list headers: Header list containing fields like 'Host','User-Agent'.
    :param dict details: Request specific details dictionary like body and method of the request.
    :param str search_string: String to search for in the response to the request. By default remains None.

    :raises ValueError: When Url is invalid or unsupported request method is passed.

    :return: Generated php script to send the request.
    :rtype:`str`
    """
    method = details['method'].lower()
    url = get_url(details['Host'], details['pre_scheme']) + details['path']
    if not check_valid_url(url):
        raise ValueError("Invalid URL '%s'." % url)

    encoding_list = ['head', 'options', 'get']
    if details['data'] and (method in encoding_list):
        encoded_data = quote(details['data'], '')
        url = url + encoded_data

    skeleton_code = php_template.begin_code.format(
        url=url) + generate_request_headers(headers) + generate_proxy_code(details)
    if method == 'get':
        pass
    elif method == 'post':
        skeleton_code += generate_post_body_code(post_body=details['data'])
    else:
        raise ValueError("'%s' is not supported. Only GET and POST requests are supported yet!" % details['method'])

    skeleton_code += generate_https_code(url)
    skeleton_code += generate_search_code(search_string)
    return skeleton_code


def generate_request_headers(headers=[]):
    """Place the request headers in php script from header dictionary.

    :param list headers: Headers list containing fields like 'Host','User-Agent'.

    :return: A string of php code which places headers in the request.
    :rtype:`str`
    """
    skeleton_code = ""
    for item in headers:
        header, value = item.split(":", 1)
        skeleton_code += php_template.request_header.format(header=str(header), header_value=str(value))
    return skeleton_code


def generate_post_body_code(post_body=''):
    """Generate body code for the php script.

    :param str post_body: Body of the request to be sent.

    :return: php script snippet with the body code.
    :rtype: `str`
    """
    return php_template.post_body_code.format(post_body=post_body.replace("'", "\\'"))


def generate_proxy_code(details={}):
    """Generate proxy code for the php script.

    :param dict details: Dictionary of request details containing proxy specific information.

    :return: php script snippet with the proxy code.
    :rtype: `str`
    """
    if 'proxy_host' and 'proxy_port' in details:
        proxy = '%s:%s' % (details['proxy_host'], details['proxy_port'])
        skeleton = php_template.proxy_code.format(proxy=proxy)
        return skeleton
    return ''


def generate_search_code(search_string=''):
    """Generate search code for the php script.

    :param str search_string: String to be found in the HTTP response from the server.

    :return: php script snippet with the HTTP response search feature.
    :rtype: `str`
    """
    if search_string:
        return php_template.body_code_search.format(search_string=search_string.replace("'", "\\'"))
    else:
        return php_template.body_code_simple


def generate_https_code(url):
    """Dummy function.

    :param str url: URL for the request.

    :return: Empty String
    :rtype:`str`
    """
    return ''
