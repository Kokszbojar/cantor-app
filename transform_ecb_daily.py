import xml.etree.ElementTree as ET

from retrieve_data import retrieve
from export_data import create_file

xml_string = retrieve('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')

root = ET.fromstring(xml_string)

currency_dict = {}
currency_rates = {}

for element in root.iter('{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube'):
    currency = element.attrib.get('currency')
    rate = element.attrib.get('rate')
    if currency and rate:
        currency_rates[currency] = float(rate)
    elif element.attrib.get('time') is not None:
        time = element.attrib.get('time')

currency_dict[time] = currency_rates


def print_data():
    for time, rates in currency_dict.items():
        print("Date:", time)
        for currency, rate in rates.items():
            print(currency, ':', rate)


create_file(currency_dict, time)
