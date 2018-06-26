from scrapy import cmdline


cmdline.execute("scrapy crawl investment -o out.csv".split())