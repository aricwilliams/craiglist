# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://wilmington.craigslist.org/']
    start_urls = ['https://wilmington.craigslist.org/search/jjj?query=it+jobs']

    def parse(self, response):
         title_list = response.xpath('//li[@class="result-row"]')
         for listing in title_list:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            text = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield { 'Date': date,
                    'Link': link,
                    'Text': text}



         url_nextpage = response.xpath('//a[text() = "next > "]/@href').extract_first()
         if url_nextpage:
            yield scrapy.request(response.urljoin(url_nextpage), callback=self.parse)
