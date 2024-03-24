import xml.etree.ElementTree as ET

from datetime import date

from retrieve_data import retrieve
from export_data import create_file, upload_data

xml_string = retrieve('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')

root = ET.fromstring(xml_string)

currency_dict = {}
currency_rates = {}

for element in root.iter('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
    currency = element.attrib.get('currency')
    rate = element.attrib.get('rate')
    if currency and rate:
        currency_rates[currency] = float(rate)

today = date.today()
time = today.strftime("%Y-%m-%d")
currency_dict[time] = currency_rates


def print_data(c_dict):
    for time, rates in c_dict.items():
        print("Date:", time)
        for currency, rate in rates.items():
            print(currency, ':', rate)


file = create_file(currency_dict, time)
upload_data(file, "river-device-417615", "river-device-417615.sm.daily-rates")
