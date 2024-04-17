from crawler.common import get_page_source, extract_number


class ABC:
    def __init__(self, item_code):
        self.item_code = item_code

    def crawl(self):
        url = 'https://dienmayabc.com/tim?q={}'.format(self.item_code.lower())
        page_soup = get_page_source(url=url)
        list_results = page_soup.find('div',{'class':'product-list'}).find_all('div', {'class': 'product'})
        if len(list_results) != 0:
            for result in list_results:
                price_text = result.find('p', {'class': 'price'}).text.strip()
                price = extract_number(price_text)[:-2]
                return price
        else:
            return None
