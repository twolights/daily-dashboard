from bs4 import BeautifulSoup
from datetime import datetime
import os
import redis
import simplejson as json
import sys
import urllib2

REDIS_CURRENCY_DATES_KEY_FORMAT='currency:%s:dates'
REDIS_CURRENCY_RATES_KEY_FORMAT='currency:%s:rate'

TABLE_ROWS_TO_SKIP=2

def fetch_single_row(r, dates_key, rates_key, row):
    tds = row.find_all('td')
    date = tds[0].a.get_text()
    ordinal = datetime.strptime(date, '%Y/%m/%d').toordinal()
    buy_rate = tds[2].get_text()
    sell_rate = tds[3].get_text()

    r.zadd(dates_key, date, ordinal)
    r.hset(rates_key, date, json.dumps({ 'buy': buy_rate, 'sell': sell_rate }))

def fetch_bank_of_taiwan_rate(currency, fetch_all):
    host, port = os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', 6379)
    r = redis.Redis(host, port)
    bot_url = 'http://rate.bot.com.tw/xrt/quote/l6m/%s?Lang=zh-TW' % currency
    dates_key = REDIS_CURRENCY_DATES_KEY_FORMAT % currency
    rates_key = REDIS_CURRENCY_RATES_KEY_FORMAT % currency
    content = urllib2.urlopen(bot_url).read()
    soup = BeautifulSoup(content, 'html.parser')

    table = soup.table
    stop = -1
    if not fetch_all:
        stop = TABLE_ROWS_TO_SKIP + 1
    pipeline = r.pipeline()
    for row in table.find_all('tr')[TABLE_ROWS_TO_SKIP:stop]:
        fetch_single_row(pipeline, dates_key, rates_key, row)
    pipeline.execute()

if __name__ == '__main__':
    currency = sys.argv[1]
    fetch_all = int(sys.argv[2]) == 1
    fetch_bank_of_taiwan_rate(currency, fetch_all)
