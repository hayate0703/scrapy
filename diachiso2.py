#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import logging
import requests
import utils
from utils import write_csv_file_unicode
import unicodecsv as csv
from database import session, Crawler
#import extractor
#import exceptions

logging.basicConfig(filename='log.txt',
                    format='%(levelname)s: %(message)s',
                    level=logging.INFO
                    )

logger = logging.getLogger(__name__)

sid = {'Benh vien':256, 'Nha thuoc':316, 'Phong kham xet nghiem':318, 'Thiet bi y te':330, 'Rang ham mat':536, 'Kham phu san':537, 'Y hoc co truyen':538,
        'Trung tam y te':539, 'Thu y': 541, 'Bac si gia dinh': 1031, 'Tu van dinh duong':1035, 'Da lieu':1039, 'Phong kham da khoa':1040,
        'Phong kham dong y':1041, 'Phong kham mat':1042, 'Phong kham nhi':1043, 'Phong kham Tai-Mui-Hong':1046, 'San pham cham soc suc khoe':1047,
        'Tam ly tri lieu':1048, 'Thuoc dong y':1049, 'Thuc pham chuc nang tai Ha Noi':1050, 'Trung tam giao duc suc khoe':1053, 'To chuc y te':1054
        }

DIACHISO_LINKS = ['http://diachiso.vn/Shop/CityPage_LoadShopBySubServiceIdAndFilterId?pageindex=1&pagesize=1000&sid={}&fid=&cityid=3&parentSid=520'.format(sid[k])
    for k in sid]

'''
def data_from_place(place):
    loc = place['geometry']['location']
    out = (place['place_id'], str(loc['lat']), str(loc['lng']))
    return out
'''

def xtract(response, xpath, allow_empty=True):
    if allow_empty:
        try:
            return response.xpath(xpath).extract()[0].strip()
        except IndexError:
            return ''
    else:
        return response.xpath(xpath).extract()[0].strip()


class DcsItem(scrapy.Item):
    address = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    #phone = scrapy.Field()
    mail = scrapy.Field()
    web = scrapy.Field()
    name = scrapy.Field()
    mobile = scrapy.Field()
    photo = scrapy.Field()


class Diachiso(scrapy.Spider):
    name = 'diachiso'
    allowed_domains = ["diachiso.vn"]

    start_urls = ['http://diachiso.vn/Shop/CityPage_LoadShopBySubServiceIdAndFilterId?pageindex=1&pagesize=1000&sid={}&fid=&cityid=3&parentSid=520'.format(sid[k])
    for k in sid]

    def parse(self, response):
        for url in response.xpath('//div[@class="media-body"]/h4/a/@href').extract():
            full_url = response.urljoin(url)
            yield scrapy.Request(full_url, callback=self.parse_data)

    def parse_data(self, response):
        item = DcsItem()

        MOBILE = "icon-phone-sign"
        ADDR = "icon-map-marker"
        PHONE = "metrouicss icon-mobile"
        MAIL = "icon-envelope-alt"
        WEB = "icon-globe"

        for li in response.xpath("//div[@class='who span7']/ul/li"):
            if ADDR in li.extract():
                item['address'] = xtract(li, "text()")
            if MAIL in li.extract():
                item['mail'] = xtract(li, "text()")
            if WEB in li.extract():
                item['web'] = xtract(li, "text()")
            if MOBILE in li.extract():
                item['mobile'] = li.xpath('text()').extract()[1]
            '''
            if PHONE in li.extract():
                phone = xtract(li, "text()")
            '''

        item['name'] = response.xpath("//div[@class='who span7']/ul/li/h1/text()").extract()
        item['lat'] = response.xpath("//script").re("var lat =.*")[0].split()[2].split('=')[1].split(';')[0].split("'")[1]
        item['lng'] = response.xpath("//script").re("var lng =.*")[0].split()[3].split(';')[0].split("'")[1]

        try:
            item['photo'] = 'diachiso.vn'+str(response.xpath('//div[@class="span3"]/a/div/img/@src').extract()[0])
        except IndexError:
            item['photo'] = ''
        
        yield item
        
        '''
        place = dict(
            place_id='',
            source='diachiso.vn',
            lat=lat,
            long=lng,
            name=xtract(response, "//div/h1/span/text()"),
            vicinity=address,
            street=",".join(address.split(',')[:-2]),
            district=address.split(',')[-2].strip(),
            province=address.split(',')[-1].strip(),
            photo=photo,
            phone=mobile,
            website=web,
            types='health',
            opening=''
            )
        '''
        
        