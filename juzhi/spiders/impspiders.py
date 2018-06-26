#-*-coding utf-8-*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import InvestmentItem

class InvestmentSpider(scrapy.Spider):
    name = "investment"
    #allowed_domains = ['www.58ztr.com']
    start_urls = ["https://voice.itjuzi.com/?cat=5066"]

    def parse(self, response):
        #提取列表中每一个新闻的链接
        #le = LinkExtractor(restrict_css='ul#articleList>li>h3')

        #for link in le.extract_links(response):
            #yield scrapy.Request(link.url, callback=self.parse_investment())

        link = response.css('h1.entry-title>a::attr(href)').extract()
        #link = response.css('ul#articleList>li>h3>a::attr(href)').extract()
        for one in link:
            url = response.urljoin(one)
            yield scrapy.Request(url=url, callback=self.parse_investment)

        # for num in range(1, 180):
        #     next_link = "http://www.58trz.com/zixun_149.html?page="
        #     next_link += str(num)
        #     print(next_link)
        #     yield scrapy.Request(url=next_link, callback=self.parse)

        # 提取下一页
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
             extract_first().replace(u'\u3000\u3000', u'\n').replace(u'\r\n', u'\n').replace(u'\t\t\t\t\t\t\n', u'\n')\
             .replace(u'\t\t\t\t\t', u'')
        item['source'] = response.xpath('//header[@class="entry-header"]/div[@class="entry-meta"]/span[@class="byline"]/span/a/text()').extract_first()
        item['link'] = response.url

        yield item

