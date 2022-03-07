import requests
import json
from config import keys

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException('Введенные валюты совпадают')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюты {base} нет в базе')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюты {quote} нет в базе')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Введенное количество {amount} не является числом')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_price = amount * json.loads(r.content)[quote_ticker]
        return total_price