# -*- coding: utf-8 -*-

import OandaAPI
import json
import csv

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

    response = OandaAPI.APIAgent().requests_api(query_type, option)
    candles = json.loads(response.text)[query_type]

    with open('Data/' + currency_pair + '.csv', "w") as file:
        csv_file = csv.writer(file, lineterminator='\n')
        csv_file.writerow(candles[0].keys())  # header row
        for candle in candles:
            csv_file.writerow(candle.values())
