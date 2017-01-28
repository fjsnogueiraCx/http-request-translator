import unittest

from hrt.interface import HttpRequestTranslator


class TestTranslator(unittest.TestCase):

    ###
    # translator.parse_raw_request
    ###
    def test_parse_raw_request_http_version_with_path(self):
        for i in range(0, 10):
            for j in range(0, 10):
                raw_request = "GET /robots.txt HTTP/%d.%d\n"\
                              "Host: foo.bar" % (i, j)
                self.assertEqual(
                    HttpRequestTranslator(request=raw_request)._parse_request(),
                    (
                        ['Host: foo.bar'],
                        {
                            'protocol': 'HTTP',
                            'pre_scheme': '',
                            'Host': 'foo.bar',
                            'version': '%d.%d' % (i, j),
                            'path': '/robots.txt',
                            'method': 'GET',
                            'data': ''
                        }
                    ),
                    'Invalid parsing of HTTP/%d.%d request!' % (i, j))

    def test_parse_raw_request_http_version_invalid(self):
        raw_request = "GET /\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar'],
                {
                    'protocol': '',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '',
                    'path': '',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of request!')
        raw_request = "GET / HTTP//1.b\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '/1.b',
                    'path': '/',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP//1.b request!')

    def test_parse_raw_request_http_with_parameter(self):
        raw_request = "GET /?foo=bar HTTP/1.1\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '1.1',
                    'path': '/?foo=bar',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of request with parameter in path!')

    def test_parse_raw_request_http_with_comment(self):
        raw_request = "GET /#foo=bar HTTP/1.1\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '1.1',
                    'path': '/#foo=bar',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of request with comment in path!')

    def test_parse_raw_request_http_with_coma(self):
        raw_request = "GET /;foo=bar HTTP/1.1\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '1.1',
                    'path': '/;foo=bar',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of request with coma in path!')

    def test_parse_raw_request_https_domain_no_port(self):
        raw_request = "GET https://google.com/robots.txt HTTP/1.1\n"\
                      "Host: google.com"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: google.com'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': 'google.com',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with domain host!')

    def test_parse_raw_request_https_domain_port(self):
        raw_request = "GET https://google.com:31337/robots.txt HTTP/1.1\n"\
                      "Host: google.com:31337"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: google.com:31337'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': 'google.com:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with domain host and custom port!')

    def test_parse_raw_request_https_ipv4_no_port(self):
        raw_request = "GET https://127.0.0.1/robots.txt HTTP/1.1\n"\
                      "Host: 127.0.0.1"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: 127.0.0.1'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '127.0.0.1',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with IPv4 host!')

    def test_parse_raw_request_https_ipv4_port(self):
        raw_request = "GET https://127.0.0.1:31337/robots.txt HTTP/1.1\n"\
                      "Host: 127.0.0.1:31337"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: 127.0.0.1:31337'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '127.0.0.1:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with IPv4 host and custom port!')

    def test_parse_raw_request_https_ipv6_no_port(self):
        raw_request = "GET https://[::1]/robots.txt HTTP/1.1\n"\
                      "Host: [::1]"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: [::1]'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '[::1]',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with IPv6 host!')

    def test_parse_raw_request_https_ipv6_port(self):
        raw_request = "GET https://[::1]:31337/robots.txt HTTP/1.1\n"\
                      "Host: [::1]:31337"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: [::1]:31337'],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': '[::1]:31337',
                    'version': '1.1',
                    'path': '/robots.txt',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with IPv6 host and custom port!')

    def test_parse_raw_request_multiple_host_header(self):
        raw_request = "GET https://foo.bar HTTP/1.1\n"\
                      "Host: foo.bar\n"\
                      "HoSt: foo.bar\n"\
                      "HOST: foo.bar \n"\
                      "host: foo.bar\n"\
                      "host:     foo.bar\n"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                [
                    'Host: foo.bar',
                    'HoSt: foo.bar',
                    'HOST: foo.bar ',
                    'host: foo.bar',
                    'host:     foo.bar',
                ],
                {
                    'protocol': 'HTTP',
                    'pre_scheme': 'https://',
                    'Host': 'foo.bar',
                    'version': '1.1',
                    'path': '',
                    'method': 'GET',
                    'data': ''
                }
            ),
            'Invalid parsing of HTTP request with multiple Host headers!')

    def test_parse_raw_request_invalid_header(self):
        raw_request = "GET https://foo.bar HTTP/1.1\n"\
                      "Host"
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request)._parse_request()

    def test_parse_raw_request_no_path(self):
        raw_request = "GET\n"\
                      "Host: foo.bar"
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request)._parse_request()

    def test_parse_raw_request_empty(self):
        raw_request = ''
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request)._parse_request()

    def test_parse_raw_request_post(self):
        raw_request = "POST /\r\n"\
                      "Host: foo.bar\r\n"\
                      "Content-Length: 2\r\n"\
                      "\r\n\r\n"\
                      "{}\r\n"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request)._parse_request(),
            (
                ['Host: foo.bar', 'Content-Length: 2'],
                {
                    'protocol': '',
                    'pre_scheme': '',
                    'Host': 'foo.bar',
                    'version': '',
                    'path': '',
                    'method': 'POST',
                    'data': '{}'
                }
            ),
            'Invalid parsing of request!')

    def test_extract_request_details(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        my_hrt = HttpRequestTranslator(request=raw_request)
        my_hrt._extract_request_details()
        self.assertEqual(
            my_hrt.headers,
            ['Host: foo.bar'],
            'Invalid parsing of request!')

    def test_extract_request_details_with_data(self):
        raw_request = "POST /\r\n"\
                      "Host: foo.bar\r\n"\
                      "Content-Length: 2"
        my_hrt = HttpRequestTranslator(request=raw_request, data='{}')
        my_hrt._extract_request_details()
        self.assertEqual(
            my_hrt.headers,
            ['Host: foo.bar', 'Content-Length: 2'],
            'Invalid parsing of request!')
        self.assertEqual(
            my_hrt.data,
            '{}',
            'Invalid extraction of request details!')

    def test_extract_request_details_with_proxy_no_port(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request, proxy='127.0.0.1')

    def test_extract_request_details_with_proxy_http_no_port(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request, proxy='http://127.0.0.1')

    def test_extract_request_details_with_proxy_invalid(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        with self.assertRaises(ValueError):
            HttpRequestTranslator(request=raw_request, proxy='http127.0.0.1')

    def test_extract_request_details_with_proxy_valid(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        my_hrt = HttpRequestTranslator(request=raw_request, proxy='127.0.0.1:8000')
        my_hrt._extract_request_details()
        self.assertEqual(
            my_hrt.details,
            {
                'proxy_host': 'http://127.0.0.1',
                'path': '',
                'data': '',
                'version': '',
                'method': 'GET',
                'pre_scheme': '',
                'Host': 'foo.bar',
                'proxy_port': '8000',
                'protocol': ''
            },
            'Invalid extraction of request details!')

    def test_extract_request_details_with_proxy_http_valid(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        my_hrt = HttpRequestTranslator(request=raw_request, proxy='http://127.0.0.1:8000')
        my_hrt._extract_request_details()
        self.assertEqual(
            my_hrt.details,
            {
                'proxy_host': 'http://127.0.0.1',
                'path': '',
                'data': '',
                'version': '',
                'method': 'GET',
                'pre_scheme': '',
                'Host': 'foo.bar',
                'proxy_port': '8000',
                'protocol': ''
            },
            'Invalid extraction of request details!')

    def test_generate_code_default(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request).generate_code(),
            {'bash': '#!/usr/bin/env bash\ncurl -v --request GET http://foo.bar  --header "Host: foo.bar"  --include'},
            'Invalid code generation!')

    def test_generate_code_default_empty(self):
        raw_request = "GET /\r\n"\
                      "Host: foo.bar"
        self.assertEqual(
            HttpRequestTranslator(request=raw_request, languages=[]).generate_code(),
            {},
            'Invalid code generation!')


if __name__ == '__main__':
    unittest.main()
