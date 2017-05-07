import os
import redis
import simplejson as json
import sys
import urllib2

REDIS_CRYPTOCURRENCY_KEY_FORMAT='cryptocurrency:%s'

def fetch_cryptocurrency_rate(currency):
    host, port = os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', 6379)
    r = redis.Redis(host, port)

    url = 'https://btc-e.com/api/3/ticker/%s' % currency
    content = urllib2.urlopen(url).read()
    result = json.loads(content)[currency]

    key = REDIS_CRYPTOCURRENCY_KEY_FORMAT % currency
    timestamp = float(result['updated'])
    buy_rate = result['buy']
    sell_rate = result['sell']
    r.zadd(key, json.dumps({ 'buy': buy_rate, 'sell': sell_rate }), timestamp)

if __name__ == '__main__':
    currency = sys.argv[1]
    fetch_cryptocurrency_rate(currency)
