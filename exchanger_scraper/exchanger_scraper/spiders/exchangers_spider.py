import scrapy


class ExchangerSpider(scrapy.Spider):
    name = "exchanger"

    start_urls = [
        "https://bank.gov.ua/control/uk/curmetal/detail/currency?period=daily"
    ]

    def parse(self, response):
        responses = response.xpath('//*[@id="exchangeRates"]//tbody//tr')
        for row in responses:
            currency = row.xpath("td[4]//text()").extract()
            official_rate = row.xpath("td[5]//text()").extract()
            alphabetic_code = row.xpath("td[2]//text()").extract()
            yield {
                "url": "https://bank.gov.ua/control/uk/curmetal/detail/currency?period=daily",
                "digital_code": row.xpath("td[1]//text()").extract(),
                "alphabetic_code": [line.strip() for line in alphabetic_code],
                "number_of_currency_units": row.xpath("td[3]//text()").extract(),
                "currency_name": [line.strip() for line in currency],
                "official_rate": official_rate,
            }
