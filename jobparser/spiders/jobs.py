import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class JobsSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        vacancy_source = response.xpath("//a[@data-qa='vacancy-company-name']/@href").extract_first()
        # vacancy_salary = response.css("p.vacancy-salary span::text").extract()
        item = JobparserItem(name=vacancy_name, salary=vacancy_salary, url=response.url, source=vacancy_source)
        yield item
