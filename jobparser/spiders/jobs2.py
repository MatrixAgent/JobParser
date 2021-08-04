import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class Jobs2Spider(scrapy.Spider):
    name = 'jobs2'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        vacancies_links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@class,'_6AfZ9')]/@href").extract()
        next_page = response.xpath("//a[contains(@class,'f-test-button-dalshe')]/@href").extract_first()
        for link in vacancies_links:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        vacancy_name = response.xpath("//h1/text()").extract_first()
        vacancy_salary = response.xpath("//span[@class= '_1OuF_ ZON4b']//text()").extract()
        vacancy_source = response.xpath("//div[@class='_3zucV FAfe0 _3fOgw']/a/@href").extract_first()
        item = JobparserItem(name=vacancy_name, salary=vacancy_salary, url=response.url, source=vacancy_source)
        yield item
