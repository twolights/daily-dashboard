import bank_of_taiwan_rate as botr
import sys

currencies = ['USD', 'JPY', 'GBP', 'EUR', 'CNY']

if __name__ == '__main__':
    fetch_all = len(sys.argv) > 2 and int(sys.argv[1]) == 1
    for currency in currencies:
        botr.fetch_bank_of_taiwan_rate(currency, fetch_all)
