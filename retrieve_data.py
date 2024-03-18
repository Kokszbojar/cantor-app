import requests

default_url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'


def retrieve(url=default_url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        content_xml = response.text
        return content_xml

    except requests.exceptions.RequestException as e:
        return f'Blad: {e}'
