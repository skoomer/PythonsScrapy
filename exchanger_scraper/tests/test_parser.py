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
        self.exchanger.create_table()
        results = self.spider.parse(self.html)
        val_str = ""
        for item in results:
            for key, value in item.items():
                if key == "digital_code":
                    self.exchanger.digital_code = int(val_str.join(value))
                elif key == "alphabetic_code":
                    self.exchanger.alphabetic_code = val_str.join(value)
                elif key == "number_of_currency_units":
                    self.exchanger.number_of_currency_units = int(val_str.join(value))
                elif key == "currency_name":
                    self.exchanger.currency_name = val_str.join(value)
                elif key == "official_rate":
                    for i in value:
                        self.exchanger.official_rate = float(i.replace(",", "."))
            self.exchanger.save()
        query = "SELECT count(*) FROM exchangecurrency;"
        self.cursor.execute(query)
        for row in self.cursor:
            self.assertEqual(row, (34,))

    def tearDown(self):
        drop = "DROP TABLE IF EXISTS exchangecurrency;"
        self.cursor.execute(drop)
