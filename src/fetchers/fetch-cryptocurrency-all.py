import cryptocurrency_rate as cr

currencies = {
    'eth_usd': 'Ethereum to USD',
    'btc_usd': 'Bitcoin to USD',
}

if __name__ == '__main__':
    for currency in currencies:
        cr.fetch_cryptocurrency_rate(currency)
