import scrapy
import xmltodict
from scrapy import Spider, Request
from ..items import IkeaUpdateItem

def get_code(code):
    list_=[code[i:i+3] for i in range(0, len(code), 3)]
    #print(list_)
    return '.'.join(list_)

class IkeaSpider(scrapy.Spider):
    name = 'ikea'
    allowed_domains = ['ikea.com.tr']

    start_urls = ['https://cdn.ikea.com.tr/sitemap/sitemap.xml']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'FEEDS':{
            'ikea_update_data.csv':{
                'format':'csv',
                'overwrite':True
            }
        }
    }
    #en_api_url='https://frontendapi.ikea.com.tr/api/search/products?language=en&Category=leather-sofas&IncludeFilters=false&StoreCode=331&sortby=None&IsSellable=&size=12&IncludeColorVariants=true'
    api_url = 'https://frontendapi.ikea.com.tr/api/search/products?language=tr&Category={cat_code}&IncludeFilters=false&StoreCode=331&sortby=None&IsSellable=&page={page}&size={size}'
   # api_url = 'https://frontendapi.ikea.com.tr/api/search/products?language=tr&Category={cat_code}&IncludeFilters=false&StoreCode=331&sortby=None&IsSellable=&page={page}&size={size}'
    def parse(self, response):
        text = response.body.decode('utf-8')
        sitemap_dict = xmltodict.parse(text)
        if sitemap_dict.get('sitemapindex'):
            for data in sitemap_dict['sitemapindex']['sitemap']:
                if data['loc'].endswith('.xml'):
                    yield Request(
                        url=data['loc'], 
                        callback=self.parse
                    )
                elif data['loc'].endswith('.axd'):
                    continue
        else:
            listing_urls = sitemap_dict['urlset']['url']
            for  url in listing_urls[:]:
                if 'kategori' in url['loc']:
                    yield Request(
                        url=url['loc'], 
                        callback=self.parse_listing
                    )
    

    def parse_listing(self, response):
        self.logger.info(response.url)
        size = 40
        cat_code = response.xpath('//input[@id="ctl00_ContentPlaceHolder1_search_categoryUrl"]/@value').get()
        url_api = self.api_url.format(
            cat_code=cat_code,
            page=1,
            size=size,
        )
        yield Request(
            url=url_api,
            callback=self.parse_api,
            meta={
                'cat_code': cat_code,
                'page': 1,
            }
        )
        
    def parse_api(self, response):
        item = IkeaUpdateItem()
        page = response.meta['page']
        cat_code = response.meta['cat_code']
        data = response.json()
        total = data['total']
        self.logger.info(f'page: {page} - total: {total}')
        products = data['products']
        for product in products[:]:
            try:
                slug=product['url']
            except:
                slug=''
                continue
            scrap_url = 'https://www.ikea.com.tr' + slug
            #scrap_url = scrap_url.replace('/urun/','/en/product/')
            price = product['price']
            name = product['title']
            category = cat_code
            try:
                qty=product['stockStatus']
            except:
                qty= 0
            try:
                old_price=product['crossPrice']
            except:
                old_price=price
            product_code = get_code(product['sprCode'])
            
            brand = 'IKEA'
            
            item['scrap_url'] = scrap_url
            item['category'] = category
            item['brand'] = brand
            item['name'] = name
            item['product_code'] = product_code
            item['price'] = price
            item['list_price'] = old_price
            item['qty'] = qty
            
            yield item
        
        if products:
            page += 1
            url_api = self.api_url.format(
                cat_code=cat_code,
                page=page,
                size=40,
            )
            
            yield Request(
                url=url_api,
                callback=self.parse_api,
                meta={
                    'cat_code': cat_code,
                    'page': page,
                }
            )

        if products:
            page += 1
            url_api = self.api_url.format(
                cat_code=cat_code,
                page=page,
                size=40,
            )
            yield Request(
                url=url_api,
                callback=self.parse_api,
                meta={
                    'cat_code': cat_code,
                    'page': page,
                }
            )