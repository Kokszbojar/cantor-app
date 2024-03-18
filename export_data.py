import json

from datetime import datetime


def create_file(transfer_data, day, scheme='ECB'):

    sql_json = []

    for date_str, rates in transfer_data.items():
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        for currency, rate in rates.items():
            record = {
                "source": scheme,
                "date": date.strftime("%Y-%m-%d"),
                "currency": currency,
                "rate": rate,
                "target_currency": "EUR"
            }
            sql_json.append(record)

    json_file = f'{scheme}_{day}.json'

    if day == 'CREATE':
        sql_json = sql_json[::-1]

    with open(json_file, 'w') as file:
        json.dump(sql_json, file, indent=4)

    return json_file
