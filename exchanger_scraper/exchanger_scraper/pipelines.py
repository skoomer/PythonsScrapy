from exchanger_scraper.connect_db import ConnectDB
from exchanger_scraper.create_table import ExchangeCurrency


ConnectDB.set_connection()


class ExchangerScraperPipeline:
    def open_spider(self, spider):
        self.connection = ConnectDB.set_connection()
        self.exchanger = ExchangeCurrency()

    def process_item(self, item, spider):

        for key, value in item.items():
            val_str = ""
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
        return item
