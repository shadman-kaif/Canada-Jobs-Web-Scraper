# -*- coding: utf-8 -*-
import scrapy

class RecursionSpider(scrapy.Spider):
    name = 'recursion'
    page_number = 2
    start_urls = ['https://www.jobbank.gc.ca/jobsearch/?fper=L&fper=P&fter=S&page=1&sort=M&fprov=ON#article-32316546']

    def parse(self, response):
        # Extracting the content using css selectors
        tag = response.xpath('//a/@href').extract()
        date = response.css('li.date::text').extract()
        title = response.css('span.noctitle::text').extract()
        location = response.css('li.location::text').extract()
        business = response.css('li.business::text').extract()

        # Removing whitespace '\n' and '\t' 
        date = map(lambda s: s.strip(), date)
        title = map(lambda s: s.strip(), title)
        location = map(lambda s: s.strip(), location)

        # Removing items in the list that are empty spaces and indexing accordingly
        title = [str for str in title if str]
        location = [str for str in location if str]

        # Extracting all the href tags to the new links
        tag = [str for str in tag if '/jobsearch/jobposting' in str]
        finalTag = ['https://www.jobbank.gc.ca' + tag for tag in tag]

        # Give the extracted content row wise
        for item in zip(date, title, location, business):
            # Create a dictionary to store the scraped info
            scraped_info = {
                'Date' : item[0],
                'Title' : item[1],
                'Location' : item[2],
                'Business' : item[3]
            }

            # Yield or give the scraped info to scrapy
            yield scraped_info
            
        for url in finalTag:
            request = scrapy.Request(url, callback=self.parse2)
            yield request

    def parse2(self, response):
        # Extracting the content using css selectors
        vacancy = response.xpath('//span/text()').extract()
        status = response.css('span.attribute-value::text').extract()
        duration = response.css('span.attribute-value::text').extract()
        jobID = response.css('span::text').extract()

        vacancy = [str for str in vacancy if "Vacanc" in str]
        vacancy.remove('Vacancies')

        del status[1]

        del duration[0]
        duration = map(lambda s: s.strip(), duration)

        jobID = [str for str in jobID if "146" in str]

        for item in zip(vacancy, status, duration, jobID):
            # Create a dictionary to store the scraped info
            scraped_info = {
                'Vacancy' : item[0],
                'Status' : item[1],
                'Duration' : item[2],
                'Job ID' : item[3]
            }

            # Yield or give the scraped info to scrapy
            yield scraped_info

            next_page = 'https://www.jobbank.gc.ca/jobsearch/?fper=L&fper=P&fter=S&page=' + str(RecursionSpider.page_number) + '&sort=M&fprov=ON#article-32316546'

            if RecursionSpider.page_number <= 5:
                RecursionSpider.page_number += 1
                yield response.follow(next_page, callback = self.parse)