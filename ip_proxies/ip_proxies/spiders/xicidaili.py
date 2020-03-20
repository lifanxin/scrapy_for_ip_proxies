# -*- coding: utf-8 -*-
import time
import scrapy
from ..items import IpProxiesItem


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']

    def parse(self, response):
        ip_list = response.xpath('//table[@id="ip_list"]//tr[position()>1]')
        for ip_info in ip_list:
            ip_proxy = IpProxiesItem()
            ip_proxy['ip'] = ip_info.xpath('./td[2]/text()').extract_first()
            ip_proxy['port'] = ip_info.xpath('./td[3]/text()').extract_first()
            ip_proxy['address'] = ip_info.xpath(
                './td[4]/a/text()').extract_first()
            ip_proxy['protocol'] = ip_info.xpath(
                './td[6]/text()').extract_first()
            ip_proxy['ttl'] = ip_info.xpath('./td[9]/text()').extract_first()
            yield ip_proxy

        next_url = response.xpath('//a[text()="下一页 ›"]/@href').extract_first()
        next_url = response.urljoin(next_url)

        print('new_page {}'.format(next_url))
        time.sleep(2)
        if next_url:
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )
