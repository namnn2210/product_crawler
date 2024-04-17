from crawler.common import get_page_source, extract_number



class DMX:
    def __init__(self, item_code):
        self.item_code = item_code

    def crawl(self):
        url = 'https://www.dienmayxanh.com/search?key={}'.format(self.item_code.lower())
        page_soup = get_page_source(url=url)
        cate_search = page_soup.find('div', {'class': 'filter-catesearch'})
        if cate_search:
            list_results = cate_search.find('ul',{'class': 'listproduct'}).find_all('li', {'class': 'item'})
            if len(list_results) != 0:
                for result in list_results:
                    product_url = 'https://www.dienmayxanh.com{}'.format(result.find('a',{'class':'main-contain'})['href'])
                    product_soup = get_page_source(url=product_url)
                    images,brand, promo = self.get_product_info(product_soup)
                    name = result.find('h3').text.strip()
                    price_div = result.find('strong', {'class': 'price'})
                    if price_div:
                        price = extract_number(price_div.text.strip())
                    else:
                        price = None
                    return price, brand,name, images, promo
        else:
            return None, None, None, None, None
        
    def get_product_info(self, product_soup):
        images = ','.join([item['data-src'] for item in product_soup.find('div',{'class':'detail-slider'}).find_all('img', {'class': 'owl-lazy'})])
        brand = product_soup.find('li',{'data-index':'99999'}).find('div',{'class':'liright'}).text.strip().replace('Xem thông tin hãng','').replace('.','')
        promo_div = product_soup.find('div',{'class':'pr-item'})
        if promo_div:
            promo = ','.join([item.text.strip().replace('(Xem chi tiết tại đây)','') for item in promo_div.find_all('div',{'class':'divb-right'})])
        else:
            promo = None
        return images, brand, promo
        
