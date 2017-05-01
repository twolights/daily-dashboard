from flask import Flask, jsonify, render_template
import os
import redis
import simplejson as json

app = Flask(__name__)
app.debug = True

@app.route('/daevanchen')
def main():
    currencies = ['USD', 'JPY', 'GBP']
    return render_template('index.html', currencies=currencies)

@app.route('/currency/<currency>')
def currency(currency):
    REDIS_CURRENCY_DATES_KEY_FORMAT='currency:%s:dates'
    REDIS_CURRENCY_RATES_KEY_FORMAT='currency:%s:rate'

    dates_key = REDIS_CURRENCY_DATES_KEY_FORMAT % currency
    rates_key = REDIS_CURRENCY_RATES_KEY_FORMAT % currency

    host, port = os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', 6379)
    r = redis.Redis(host, port)
    dates = [d for d in reversed(r.zrevrange(dates_key, 0, 60))]
    rates = r.hmget(rates_key, *dates)
    labels = [dates[i][5:] if i % 3 == 0 else '' for i in range(0, len(dates))]
    buy = []
    sell = []
    for k in range(0, len(dates)):
        rate = json.loads(rates[k])
        buy.append(rate['buy'])
        sell.append(rate['sell'])
    data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Buy',
                'data': buy,
                'backgroundColor': 'rgba(100,100,255,0.8)',
                'pointRadius': 0,
                'pointHitRadius': 5,
                'pointHoverRadius': 5,
            },
            {
                'label': 'Sell',
                'data': sell,
                'backgroundColor': 'rgba(200,200,255,0.8)',
                'pointRadius': 0,
                'pointHitRadius': 5,
                'pointHoverRadius': 5,
            },
        ]
    }
    return jsonify(data)

@app.route('/dwarfpool/')
def dwarfpool_status():
    return ''
