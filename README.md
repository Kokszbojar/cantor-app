Recruitment task

Environment in requirements.txt

Code is divided into few parts:
1 - retrieve data 
2 - transform data
3 - export data

Unfortunately due to lack of free time i focused only on making the app with usage of European Central Bank rates

There are 2 scripts to create and upload data to the warehouse:
1 - Last 90 working days (only used with empty database)
2 - Today (added to existing database)

For target currency to change please set it with function create_file(..., target_currency='EUR') (EUR set to default)
To select database set it with function upload_data(file, project_id="project_id", table_id="project_id.database_id.table_id")

So I didn't make any tests just the manual debugging with flake8

To make it work it needs also a cronjob set in crontab to just execute transform_ecb_daily.py script every day

To deploy gcloud function I used:
gcloud functions deploy calculate --runtime python38 --trigger-http --allow-unauthenticated
It worked in google console test so should work for you as well

Input values:
- value (number, eg. 50)
- currency (string, eg. 'PLN')
- target_currency (string, eg. 'USD')
- date (string, eg. '2024-03-24', exact format YYYY-MM-DD)

Output values:
- converted_value (number, eg. 12.5)
