import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['webscraper.io']
    start_urls = [
        'https://webscraper.io/test-sites/e-commerce/static/computers/laptops']
    index_url = 'https://webscraper.io'

    def parse(self, response):

        title_xpath = '//*[contains(@class, "title")]/@title'
        price_xpath = '//*[contains(@class, "price")]/text()'

        titles = response.xpath(title_xpath)
        prices = response.xpath(price_xpath)

        for title, price in zip(titles, prices):
            yield {'title': title.get(), 'price': price.extract()}

        next_relative_page = response.xpath('//a[@rel="next"]/@href').get()
        next_page = f'{self.index_url}{next_relative_page}'

        if next_page:
            yield scrapy.Request(url=next_page)
