# -*- coding: utf-8 -*-
import scrapy
import re

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

        # Salary extracts, min and max salaries are ranges for jobs
        salary_min_value = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='minValue']::text").extract()
        salary_max_value = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='maxValue']::text").extract()
        salary_unit = response.css("ul.job-posting-brief.colcount-lg-2 span[property*='unitText']::text").extract()

        postal_code = response.css("p.nomargin::text").extract()

        # Removing unnecessary whitespace and words from strings in list
        date = map(lambda s: s.strip(), date)
        date = map(lambda s: s.strip(" Posted on "), date)

        # Removing the comma at the end of the location as it's extracted with a comma at the end
        location = [x[:-1] for x in location]

        # Going through span tag to find the vacancy number
        vacancy = [str for str in vacancy if "vacanc" in str]
        vacancy.remove('vacancies') # Remove one instance of "vacancies" string that comes in extract before

        # Extract the number of vacancies as a string in list 
        vacancy = [int(word) for word in vacancy[0].split() if word.isdigit()]
        vacancy = int(''.join(map(str,vacancy)))
        vacancy = [str(vacancy)]

        # Status and duration cleaning
        del status[1]
        del duration[0]
        duration =  map(lambda s: s.strip(), duration)

        if len(business) == 0:
            business = response.css("span.business span[property*='name'] strong::text").extract()

        if len(hours) == 0:
            hours = [""]

        # Stripping of "hours per week" string which is not needed
        hours = map(lambda s: s.strip("hours per week"), hours)

        # Adding dollar assign before the salaries
        sal_max = ["$" + salary_max_value for salary_max_value in salary_max_value]
        sal_min = ["$" + salary_min_value for salary_min_value in salary_min_value]

        # Stripping of the "NOC" keyword from NOC Number extract
        noc_number = map(lambda s: s.strip("NOC "), noc_number)

        """
        Error Checking
        """
        if len(sal_max) == 0:
            sal_max = [""]
        
        if len(sal_min) == 0:
            sal_min = [""]

        if len(salary_unit) == 0:
            salary_unit = [""]
        
        salary_unit = [x.lower() for x in salary_unit]

        if len(location) == 0:
            location = response.css("span.city::text").extract()
            location = [str for str in location if "\tON" in str]
            location = [''.join(item.split()) for item in location]
            location = [s.replace(',ON', '') for s in location]
            location = re.sub(r"(\w)([A-Z])", r"\1 \2", location[0])
            location = location.split(',')

        if len(location) == 0: 
            location = [""]

        if len(vacancy) == 0: 
            vacancy = [""]

        if len(postal_code) == 0:
            postal_code = [""]

        if len(business) == 0:
            business = [""]

        if bool(date) == False:
            date = [""]

        if bool(noc_number) == False:
            noc_number = [""]

        if bool(hours) == False:
            hours = [""]
        
        if bool(duration) == False:
            duration = [""]

        # Checking for prefix string in Job ID
        jobID = [str for str in jobID if "147" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "146" in str]
        if len(jobID) == 0:
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "149" in str]
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
            jobID = response.css('span::text').extract()
            jobID = [str for str in jobID if "148" in str]
        if len(jobID) == 0:
            jobID = [""]

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
