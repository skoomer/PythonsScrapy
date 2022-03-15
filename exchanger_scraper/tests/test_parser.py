import unittest
from scrapy.selector import Selector
from exchanger_scraper.connect_db import ConnectDB
from exchanger_scraper.create_table import ExchangeCurrency
from exchanger_scraper.exchanger_scraper.pipelines import ExchangerScraperPipeline
from exchanger_scraper.exchanger_scraper.spiders.exchangers_spider import (
    ExchangerSpider,
)

ConnectDB.set_connection()


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.spider = ExchangerSpider()
        self.pipeline = ExchangerScraperPipeline()
        self.html = Selector(text=open("exchanger-markets.html", "r").read())
        self.cursor = ConnectDB._get_cursor()
        self.exchanger = ExchangeCurrency()

    def _test_item_results(self, results, expected_length):
        list_item = []
        for item in results:
            list_item.append(item.items())
            self.assertIsNotNone(item["alphabetic_code"])
        self.assertEqual(len(list_item), expected_length)

    def test_parse(self):
        results = self.spider.parse(self.html)
        self._test_item_results(results, 34)

    def test_check_valid_values_save_to_db(self):
        item = {
            "digital_code": ["933"],
            "alphabetic_code": ["BYN"],
            "number_of_currency_units": ["1"],
            "currency_name": ["Білоруський рубль"],
            "official_rate": ["10,9628"],
        }
        self.exchanger.create_table()
        self.pipeline.open_spider(self.spider)
        self.pipeline.process_item(item, self.spider)
        query = "SELECT count(*) FROM exchangecurrency;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (1,))

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS exchangecurrency;"
        self.cursor.execute(drop)
