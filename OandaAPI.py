# -*- coding: utf-8 -*-
import requests

# http://developer.oanda.com/rest-live/introduction/

class APIAgent(object):# {{{
    base_domain = 'api-fxpractice.oanda.com'
    url_base = 'https://{}/v1/'.format(base_domain)
    APIToken = "42428628422b4cfc3f383d83b8f09c91-38edc7793a04a9b0d93602f3a309c825"

    def requests_api(self, query_type, option, payload=None):
        auth = 'Bearer {}'.format(self.APIToken)
        headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
                   'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
                   'Content-type': 'application/json; charset=utf-8',
                   'Authorization': auth}
        url = self.url_base + query_type + '?' + option

        if payload:
            requests.adapters.DEFAULT_RETRIES = 2
            response = requests.post(url, headers=headers, data=payload, timeout=10)
        else:
            requests.adapters.DEFAULT_RETRIES = 2
            response = requests.get(url, headers=headers, timeout=10)
        print 'REQUEST_API: {}'.format(url)
        return response# }}}

