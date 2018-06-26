#-*-coding utf-8-*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import InvestmentItem

class InvestmentSpider(scrapy.Spider):
    name = "investment"
    start_urls = ["https://voice.itjuzi.com/?cat=5066"]

    def parse(self, response):


        link = response.css('h1.entry-title>a::attr(href)').extract()
        for one in link:
            url = response.urljoin(one)
            yield scrapy.Request(url=url, callback=self.parse_investment)

        le = LinkExtractor(restrict_css='div.nav-links>div.nav-previous')
        links = le.extract_links(response)
        print(links)
        if links:
            next_url = links[0].url
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_investment(self, response):
        item = InvestmentItem()

        item['title'] = response.xpath('//header[@class="entry-header"]/h1/text()').extract_first()
        item['date'] = response.xpath('//header[@class="entry-header"]/div[@class="entry-meta"]/span/a/time/text()').extract_first()
        item['content'] = response.xpath('string(//div[@class="entry-content"])').\
             extract_first().replace(u'\t\t\n', u'\n').replace(u'\xa0\n', u'\n').replace(u'\t\t\t\t\t\t\n', u'\n')\
             .replace(u'\t\t\t', u'\n')
        item['source'] = response.xpath('//header[@class="entry-header"]/div[@class="entry-meta"]/span[@class="byline"]/span/a/text()').extract_first()
        item['link'] = response.url

        yield item

