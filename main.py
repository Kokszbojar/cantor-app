from flask import Flask, request, jsonify
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

app = Flask(__name__)


def get_rate(date, currency, target_currency):
    client = bigquery.Client()
    query = f"""
        SELECT rate, currency
        FROM `river-device-417615.sm.daily-rates`
        WHERE date = '{date}' AND (currency = '{currency}' OR currency = '{target_currency}')
    """
    try:
        query_job = client.query(query)
        results = query_job.result()
        rates = {}
        for row in results:
            rates[row.currency] = row.rate
        if len(rates.keys()) == 2:
            return rates[target_currency] / rates[currency]
        elif currency in rates.keys():
            return 1 / rates[currency]
        else:
            return rates[target_currency]
    except NotFound:
        return None


@app.route('/calculate', methods=['POST'])
def calculate(request):
    req_data = request.get_json()
    value = req_data.get('value')
    currency = req_data.get('currency')
    target_currency = req_data.get('target_currency')
    date = req_data.get('date')

    if not all([value, currency, target_currency, date]):
        return jsonify({'error': 'Missing parameters'}), 400

    rate = get_rate(date, currency, target_currency)
    if rate is None:
        return jsonify({'error': 'Rate not found'}), 400

    converted_value = value * rate

    return jsonify({'converted_value': converted_value})
