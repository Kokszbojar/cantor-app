import json

from datetime import datetime
from google.cloud import bigquery


def create_file(transfer_data, day, scheme='ECB', target_currency='EUR'):

    sql_json = []

    for date_str, rates in transfer_data.items():
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if target_currency != 'EUR':
            multiply = rates[target_currency]
        for currency, rate in rates.items():
            if currency == target_currency:
                record = {
                    "source": scheme,
                    "date": date.strftime("%Y-%m-%d"),
                    "currency": "EUR",
                    "rate": 1 / multiply,
                    "target_currency": target_currency
                }
            else:
                record = {
                    "source": scheme,
                    "date": date.strftime("%Y-%m-%d"),
                    "currency": currency,
                    "rate": rate / multiply,
                    "target_currency": target_currency
                }
            sql_json.append(record)

    json_file = f'{scheme}_{day}.json'

    if day == 'CREATE':
        sql_json = sql_json[::-1]

    with open(json_file, 'w') as file:
        for row in sql_json:
            json.dump(row, file)
            file.write('\n')

    return json_file


def upload_data(file, project_id="river-device-417615", table_id="river-device-417615.sm.daily-rates"):
    client = bigquery.Client(project=project_id)

    with open(file, "r") as f:
        rows = f.readlines()

    for row in rows:
        try:
            data = json.loads(row.strip())
            errors = client.insert_rows_json(table_id, [data])
            if errors == []:
                continue
            else:
                return ("Errors: ", errors)
        except Exception as e:
            return ("Exception:", str(e))
    return "Success"
