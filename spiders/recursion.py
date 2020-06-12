# -*- coding: utf-8 -*-
import scrapy

class RecursionSpider(scrapy.Spider):
    name = 'recursion'
    page_number = 2
    start_urls = ['https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=M&fprov=ON&page=1']

    def parse(self, response):
        # Extracting the content using css selectors
        tag = response.xpath('//a/@href').extract()

        # Extracting all the href tags to the new links
        tag = [str for str in tag if '/jobsearch/jobposting' in str]
        finalTag = ['https://www.jobbank.gc.ca' + tag for tag in tag]

        # Moving onto new tags
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
        noc_number = response.css("span.noc-no::text").extract()

        salary_min_value = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='minValue']::text").extract()
        salary_max_value = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='maxValue']::text").extract()
        salary_unit = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='unitText']::text").extract()

        postal_code = response.css("p.nomargin::text").extract()

        # Removing unnecessary whitespace and words from strings in list
        date = map(lambda s: s.strip(), date)
        date = map(lambda s: s.strip(" Posted on "), date)
        postal_code = [x.strip(' ') for x in postal_code]

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

        if len(hours) == 0:
            hours = [""]

        hours = map(lambda s: s.strip("hours per week"), hours)

        sal_max = ["$" + salary_max_value for salary_max_value in salary_max_value]
        sal_min = ["$" + salary_min_value for salary_min_value in salary_min_value]

        if len(sal_max) == 0:
            sal_max = [""]
        
        if len(sal_min) == 0:
            sal_min = [""]

        if len(salary_unit) == 0:
            salary_unit = [""]
        
        salary_unit = [x.lower() for x in salary_unit]

        noc_number = map(lambda s: s.strip("NOC "), noc_number)

        if len(location) == 0:
            location = [""]

        if len(vacancy) == 0: 
            vacancy = [""]

        if len(postal_code) == 0:
            postal_code = [""]


        # Output 
        for item in zip(title, date, location, business, vacancy, status, duration, jobID, hours, sal_min, sal_max, salary_unit, noc_number):
            # Create a dictionary to store the scraped info
            scraped_info = {
                'Title' : item[0],
                'Date' : item[1],
                'Location' : item[2],
                'Business' : item[3],
                'Vacancy' : item[4],
                'Status' : item[5],
                'Duration' : item[6],
                'Job ID' : item[7],
                'Hours per Week' : item[8],
                'Minimum Salary' : item[9],
                'Maximum Salary' : item[10],
                'Duration of Salary' : item[11],
                'NOC Number' : item[12]
            }

            # Yield or give the scraped info to scrapy
            yield scraped_info

            # Next search results
            next_page = 'https://www.jobbank.gc.ca/jobsearch/jobsearch?sort=M&fprov=ON&page=' + str(RecursionSpider.page_number)

            if RecursionSpider.page_number <= 750:
                # Increment page number
                RecursionSpider.page_number += 1
                yield response.follow(next_page, callback = self.parse)