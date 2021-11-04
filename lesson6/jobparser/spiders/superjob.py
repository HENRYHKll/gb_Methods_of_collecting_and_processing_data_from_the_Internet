import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=c%2B%2B&geo%5Bt%5D%5B0%5D=4',
                  'https://www.superjob.ru/vacancy/search/?keywords=c%2B%2B&geo%5Bt%5D%5B0%5D=10']

    def parse(self, response: HtmlResponse):
        urls = response.xpath(
            "//div[contains(@class,'f-test-vacancy-item')]//a[contains(@href, 'vakansii')]/@href").getall()
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        salary = response.xpath("//h1/following-sibling::span//text()").get()
        # vac_salary = response.css("p.vacancy-salary span::text").get()
        vac_url = response.url
        site_from = SuperjobSpider.allowed_domains[0]

        item = JobparserItem(name=vac_name, salary=salary, url=vac_url, site_from=site_from)
        yield item
