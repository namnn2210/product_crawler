import requests
from crawler.common import extract_number

class SGT:
    def __init__(self, item_code):
        self.item_code = item_code

    def crawl(self):
        url = f"https://sgt.com.vn/search?q=filter=((title:product**{self.item_code})||(title:product%20adjacent%20{self.item_code})||(titlespace:product%20contains%20{self.item_code})||(sku:product**{self.item_code})||(body:product**{self.item_code}))&view=ega.smartsearch.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            if len(results) == 0:
                return None
            price = extract_number(data['results'][0]['price'])
            return price
        else:
            return None