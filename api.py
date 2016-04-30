# -*- coding: utf-8 -*-
import requests
import json
import csv

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

if __name__ == '__main__':
    print "getting historical data ....."

    granularity = "M1"
    count = '5000' # maximum number is 5000
    candleFormat = 'midpoint' # defalut is 'bidask'
    currency_pair = "USD_JPY"
    dailyAlignment = '0'
    alignmentTimezone = 'Asia%2FTokyo'
    # start = "2001-02-03T04:05:06Z"

    query_type = 'candles'
    option = 'instrument={}&'.format(currency_pair) + \
        'count={}&'.format(count) +\
        'candleFormat={}&'.format(candleFormat) +\
        'granularity={}&'.format(granularity) +\
        'dailyAlignment={}&'.format(dailyAlignment) +\
        'alignmentTimezone={}'.format(alignmentTimezone)
        # 'start={}'.format(start)

    response = APIAgent().requests_api(query_type, option)
    candles = json.loads(response.text)[query_type]

    with open(currency_pair + '.csv', "w") as file:
        csv_file = csv.writer(file, lineterminator='\n')
        csv_file.writerow(candles[0].keys())  # header row
        for candle in candles:
            csv_file.writerow(candle.values())

