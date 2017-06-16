import os
import sys
from os import path

import numpy as np

import scrapy

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from items import FacultyItem


class FacultySpider(scrapy.Spider):
    name = "faculty"
    start_urls = [
        'http://sysbio.ucsf.edu/faculty_iframe.php?program=bi',
        'http://bioinformatics.ucsd.edu/faculty'
    ]

    UCSF_INDEX = 0
    UCSD_INDEX = 1

    def parse(self, response):
        if response.url == self.start_urls[self.UCSF_INDEX]:
            for entry in response.css('div.database-record'):

                # email, website
                links = entry.css('p a::text').extract()

                # No website
                if len(links) < 2:
                    links.append('')

                item = FacultyItem()
                item['university'] = 'UCSF'
                item['name'] = self.ucsf_name(entry)
                item['email'], item['website'] = self.ucsf_links(entry)
                item['title'] = self.ucsf_title(entry)
                item['department'] = self.ucsf_department(entry)
                item['interests'] = self.ucsf_interests(entry)
                item['photo'] = self.ucsf_photo(entry)
                yield item

        elif response.url == self.start_urls[self.UCSD_INDEX]:
            for entry in response.css('tbody tr'):
                item = FacultyItem()
                item['university'] = 'UCSD'
                item['name'] = self.ucsd_name(entry)
                item['email'], item['website'] = self.ucsd_links(entry)
                item['title'] = self.ucsd_title(entry)
                item['department'] = self.ucsd_department(entry)
                item['interests'] = self.ucsd_interests(entry)
                item['photo'] = self.ucsd_photo(entry)
                yield item
        else:
            pass

#   -------------------- UCSD Helper Methods --------------------
    def ucsf_name(self, entry):
        name = entry.css('h3::text').extract_first()

        # Name not found
        if name is None:
            return ''
        else:
            return name

    def ucsf_links(self, entry):
        # email, website
        links = entry.css('p a::text').extract()

        # No website
        if len(links) < 2:
            links.append('')

        return links[0], links[1]

    def ucsf_title(self, entry):
        title_raw = entry.css('p::text').extract()

        if len(title_raw) == 0:
            return ''
        else:
            return title_raw[0].split(',')[0]

    def ucsf_department(self, entry):
        department_raw = entry.css('p::text').extract()

        if len(department_raw) == 0:
            return ''
        else:
            return department_raw[0].split(',')[1]

    def ucsf_interests(self, entry):
        raw_interests = entry.css('p::text').extract()

        # Interests not found
        if raw_interests is None:
            return ''

        interests = raw_interests[1].split(',')
        interests = [interest.strip() for interest in interests]
        return interests

    def ucsf_photo(self, entry):
        selector = 'a.database-image-link::attr(href)'
        photo_url = entry.css(selector).extract_first()
        if photo_url is None:
            return ''
        else:
            return photo_url


#   -------------------- UCSD Helper Methods --------------------
    def ucsd_name(self, entry):
        name = entry.css('h3::text').extract_first()

        # Name not found
        if name is None:
            return ''
        else:
            return name

    def ucsd_links(self, entry):
        selector = 'td.views-field-field-people-email a::attr(href)'
        links = np.array(entry.css(selector).extract())

        # Website boolean identifier
        is_email = ['mailto' in x for x in links]

        # Email link
        email_raw = links[is_email]
        if len(email_raw) == 0:
            email = ''
        else:
            email_raw = email_raw[0]
            username = email_raw.split('>')[2].split('<')[0].strip()
            domain = email_raw.split('>')[4].split('<')[0].strip()
            email = '@'.join([username, domain])

        # Website link
        # Use non-email link as website link
        website_raw = links[['mailto' not in x for x in links]]
        if len(website_raw) == 0:
            website = ''
        else:
            website = website_raw[0].strip()

        return email, website

    def ucsd_title(self, entry):
        selector = 'td.views-field-field-people-lastname::text'
        raw_text = entry.css(selector).extract()

        # Title not found
        if len(raw_text) == 0:
            return ''

        return ''.join(raw_text).strip().split(',')[0]

    def ucsd_department(self, entry):
        selector = 'td.views-field-field-people-lastname a::text'
        return entry.css(selector).extract()

    def ucsd_interests(self, entry):
        raw_text = entry.css('p::text').extract_first()

        # Interests not found
        if raw_text is None:
            return ''

        interests = raw_text.strip(': ').split(',')
        interests = [interest.strip() for interest in interests]

    def ucsd_photo(self, entry):
        selector = 'td.views-field-field-people-photo img::attr(src)'
        photo_url = entry.css(selector).extract_first()

        # Photo url not found
        if photo_url is None:
            return ''
        return photo_url
