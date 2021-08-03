import requests
from bs4 import BeautifulSoup
import re

def produce_ebay_prices(payload: dict) -> list:
    """Asks for parameters for an item on ebay and produces sold prices for it"""

    base_url = "https://www.ebay.com/sch/"

    source = _get_url_source(base_url, payload)
    price_list = _get_source_details(source)

    return price_list


def _get_source_details(source: requests) -> list:
    """Gets the details from the html source provided and returns a list of the prices"""

    price_list = []

    soup = BeautifulSoup(source.text, features="html.parser")
    prices = soup.find_all(class_="bold bidsold")

    for price in prices:
        price_point = price.find(string=True)

        if len(price_point) <= 1:
            for pr_range in price:

                for price_range in pr_range:

                    if '$' in price_range:
                        price_list.append(float(re.sub("[^\d\.]", "", price_range)))
        else:
            price_list.append(float(re.sub("[^\d\.]", "", price_point)))

    return price_list

def _get_url_source(base_url: str, payload: dict) -> requests:
    """Takes a url string as input and returns the html source code"""

    source = requests.get(base_url, params=payload)
    return source
