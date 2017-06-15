import scrapy
from ..items import UcsfItem

class UCSFSpider(scrapy.Spider):
    name = "ucsf"
    start_urls = [
        'http://sysbio.ucsf.edu/faculty_iframe.php?program=bi'
    ]

    def parse(self, response):
        for entry in response.css('div.database-record'):
            links = entry.css('p a::text').extract()

            # No website
            if len(links) < 2:
                links.append('')

            item = UcsfItem()
            item['name'] = entry.css('h3::text').extract_first()
            item['email'] = links[0]
            item['title'] = entry.css('p::text').extract()[0].split(',')[0]
            item['department'] = entry.css('p::text').extract()[0].split(',')[1]
            item['interests'] = entry.css('p::text').extract()[1].split(',')
            item['website'] = links[1]

            yield item
