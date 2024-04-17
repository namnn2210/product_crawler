import argparse
import pandas as pd
import math
from crawler.dmx import DMX
from crawler.abc import ABC
from crawler.sgt import SGT
from crawler.common import send_telegram_message

CHAT_ID = '-1002033976688'
TOKEN = '6865061661:AAGLnymKAJjmbDmaO7gLAhz1Da0tRWScr9w'
source_excel = 'digigreen.xlsx'
parser = argparse.ArgumentParser(description='Công cụ lấy dữ liệu sản phẩm từ website')
parser.add_argument('--site', type=str, help='Site nguồn dữ liệu', default='dmx')
args = parser.parse_args()

def get_crawler(site, item_code):
    if site == 'dmx':
        return DMX(item_code=item_code)
    elif site == 'abc':
        return ABC(item_code=item_code)
    elif site == 'sgt':
        return SGT(item_code=item_code)
    else:
        print('Site nguồn không hợp lệ')

if __name__ == '__main__':
    df = pd.read_excel(source_excel)[:10]
    site = args.site
    if f'last_{site}' not in df.columns:
        df[f'last_{site}'] = ''
    if f'crawl_{site}' not in df.columns:
        df[f'crawl_{site}'] = ''
    if f'change_{site}' not in df.columns:
        df[f'change_{site}'] = 0
    for index, row in df.iterrows():
        item_code = row['ma_hang']
        print('Lấy dữ liệu mã hàng: ', item_code)
        crawler = get_crawler(args.site, item_code)
        if crawler is not None:
            if args.site == 'dmx':
                print('Site nguồn là DMX, lấy toàn bộ thông tin sản phẩm')
                price, brand, name, images,promo = crawler.crawl()
                df.loc[index, 'nhan_hieu'] = brand
                df.loc[index, 'ten_sp'] = name
                df.loc[index, 'anh_sp'] = images
                df.loc[index, 'qua_tang'] = promo
            else:
                print('Site nguồn là {}, chỉ cập nhật giá sản phẩm'.format(args.site))
                price = crawler.crawl()
            if not price:
                price = '0'
            if df.loc[index, f'last_{site}'] == '' and df.loc[index, f'crawl_{site}'] == '':
                df.loc[index, f'last_{site}'] = price
                df.loc[index, f'crawl_{site}'] = price
            else:
                df.loc[index, f'last_{site}'] = df.loc[index, f'crawl_{site}']
                df.loc[index, f'crawl_{site}'] = price
            # print(df.loc[index, f'crawl_{site}'] == df.loc[index, f'last_{site}'])
            if int(df.loc[index, f'crawl_{site}']) != int(df.loc[index, f'last_{site}']):
                alert = '*Sản phẩm biến động giá* \nMã SP: *{}* \nGiá cũ: *{}* \nGiá mới: *{}* \nNguồn cập nhật giá: *{}*'.format(item_code, df.loc[index, f'last_{site}'], df.loc[index, f'crawl_{site}'], site)
                send_telegram_message(alert, CHAT_ID, TOKEN)
            if price and price != '0' and price != 'NaN': 
                if df.loc[index, f'last_{site}'] != 0:
                    last_site = df.loc[index, f'last_{site}']
                    crawl_site = df.loc[index, f'crawl_{site}']     
                    if not math.isnan(int(last_site)) and not math.isnan(int(crawl_site)):
                        df.loc[index, f'change_{site}'] = (int(crawl_site) - int(last_site)) / int(last_site) * 100
    df.to_excel(source_excel, index=False)
