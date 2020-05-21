# -*- coding: utf-8 -*-
import scrapy

class RecursionSpider(scrapy.Spider):
    name = 'recursion'
    page_number = 2
    start_urls = ['https://www.jobbank.gc.ca/jobsearch/jobsearch?fper=F&fter=P&page=1&sort=M&fprov=ON#results-list-content']

    def parse(self, response):
        # Extracting the content using css selectors
        tag = response.xpath('//a/@href').extract()

        # Extracting all the href tags to the new links
        tag = [str for str in tag if '/jobsearch/jobposting' in str]
        finalTag = ['https://www.jobbank.gc.ca' + tag for tag in tag]

        for url in finalTag:
            yield response.follow(url, self.parse2)
            
    def parse2(self, response):                                                                                    

        # Extracting the content using css and xpath selectors
        title = response.css('span.noc-title::text').extract()
        date = response.css("span.date::text").extract()
        location = response.css("span.city span[property*='addressLocality']::text").extract()    
        business = response.css("a.external::text").extract()
        vacancy = response.xpath('//span/text()').extract()
        status = response.css('span.attribute-value::text').extract()
        duration = response.css('span.attribute-value::text').extract()
        hours = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='workHours']::text").extract()
        jobID = response.css('span::text').extract()

        # Removing unnecessary whitespace and words from strings in list
        date = map(lambda s: s.strip(), date)
        date = map(lambda s: s.strip(" Posted on "), date)
        hours = map(lambda s: s.strip(), hours)
        hours = map(lambda s: s.strip("hours per week"), hours)

        # Removing the comma at the end of the location as it's extracted with a comma at the end
        location = [x[:-1] for x in location]

        # Going through span tag to find the vacancy number
        vacancy = [str for str in vacancy if "Vacanc" in str]
        vacancy.remove('Vacancies') # Remove one instance of "Vacancies" string that comes before

        # Status and duration cleaning
        del status[1]
        del duration[0]
        duration = map(lambda s: s.strip(), duration)

        # Checking for 146 string in Job ID
        jobID = [str for str in jobID if "147" in str]

        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "146" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "145" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "144" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "143" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "142" in str]
        if len(jobID) == 0:
            jobID = [""]

        if len(business) == 0:
            business = response.css("span.business span[property*='name'] strong::text").extract()

        for item in zip(title, date, location, business, vacancy, status, duration, jobID):
            # Create a dictionary to store the scraped info
            scraped_info = {
                'Title' : item[0],
                'Date' : item[1],
                'Location' : item[2],
                'Business' : item[3],
                'Vacancy' : item[4],
                'Status' : item[5],
                'Duration' : item[6],
                'Job ID' : item[7]
            }

            # Yield or give the scraped info to scrapy
            yield scraped_info

            # Next search results
            next_page = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?fper=F&fter=P&page=' + str(RecursionSpider.page_number) + '&sort=M&fprov=ON#results-list-content'

            if RecursionSpider.page_number <= 250:
                # Incrememnt page number
                RecursionSpider.page_number += 1
                yield response.follow(next_page, callback = self.parse)