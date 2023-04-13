To get help:

$ python weather.py -h

usage: weather.py [-h] --function FUNCTION --city CITY [--year YEAR] [--month MONTH]

options:
  -h, --help           show this help message and exit
  --year YEAR          year
  --month MONTH        month, 1-12

required arguments:
  --function FUNCTION  weather function
  --city CITY          city of interest

FUNCTION is either days-of-precip or max-temp-delta.
CITY is either bos or jnu or mia.
YEAR must be between 2010-2019, inclusive.

days-of-precip only takes a city. It evaluates the
entirety of the 10 year record.

max-temp-delta takes a city, and optionally a year, or a year
and a month.

A few output jsons are included here.

For days-of-precip, the json file name is of the form
CITY_ppt.json.

For max-temp-delta, the form is CITY[YYYY][MM]_temp.json,
where YYYY and MM are included only if they were given
by the user.
