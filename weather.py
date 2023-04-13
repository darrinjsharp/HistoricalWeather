#!/opt/homebrew/bin/python3

from typing import List
from datetime import datetime
import argparse
import csv
import json
import os
import pandas as pd
import sys

'''
Script to calculate the average number of days per year a given city
had non-zero precipitation (rain or snow), or the maximum temperature
difference experienced on a single day in a specified period.
'''

def _get_args(args: List[str]):

    parser = argparse.ArgumentParser()
    required = parser.add_argument_group("required arguments")

    required.add_argument(
        "--function",
        help="weather function: days-of-precip or max-temp-delta",
        required=True,
        type=str,
    )

    required.add_argument(
        "--city",
        help="city of interest: bos, jnu, or mia",
        required=True,
        type=str,
    )

    parser.add_argument(
        "--year",
        help="year: 2010-2019 inclusive",
        type=int,
    )

    parser.add_argument(
        "--month",
        help="month: 1-12",
        type=int,
    )

    return parser.parse_args(args)

def read_data(city):
    '''
    Read in the historical data and create a data frame that contains
    only the data for the city of interest.
    '''
    
    dataFrame = pd.read_csv("noaa_historical_weather_10yr.csv")
    city_df = dataFrame[dataFrame['NAME'] == f"{city}"]

    return city_df

def days_of_precip(city: str, city_abv: str):
    '''
    Using a dataframe that contains only the city of interest, calculate
    the precipitation statistic. Note that this statistic covers all 10
    years of data.
    '''

    city_df = read_data(city)
    
    # Assume that PRCP is rain only. It is possible there could be rain
    # and snow on the same day. OR these quantities so a day with
    # rain AND snow doesn't get double counted.
    count = ((city_df['PRCP'] != 0) | (city_df['SNOW'] != 0)).sum()
    print(f"{os.linesep}10 year count of ppt days for {city_abv} = {count}.{os.linesep}")
    avg_yrly_ppt_days = format(count/10,'.1f')
    
    ppt_dict = { 
        "city": city,
        "days_of_precip": float(avg_yrly_ppt_days),
        }

    with open(f"{city_abv}_ppt.json", "w") as outfile:
        json.dump(ppt_dict, outfile)

    return

def max_temp_delta(city: str, city_abv:str, month: int, year: int):
    '''
    Using a dataframe that contains only the city of interest, calculate
    the maximum temperature statistic. Note that the period considered
    is user specified. If no month or year is given, the entire 10 year
    record is evaluated. If a year is given, that entire year is 
    evaluated. If a year and month is given, only that one month is
    evaluated.
    '''
    
    df = read_data(city)
    jsonfilename = city_abv

    if year is not None:
        # Filter the dataframe on the year.
        df = df[df['DATE'].str.startswith(f"{year}-")]
        jsonfilename = jsonfilename + str(year)

    if month is not None:
        # The dataframe was already filtered on the year above;
        # filter the dataframe on the month here.
        month = str(month).zfill(2)
        df = df[df['DATE'].str.contains(f"-{month}-",regex=False)]
        jsonfilename = jsonfilename + month
    
    # Find the index of the day with the greatest delta.
    idx = (((df['TMAX']) - (df['TMIN'])).idxmax())
    date = (df.at[idx,'DATE'])
    
    temp_change = format((df.at[idx,'TMAX'] - df.at[idx,'TMIN']),'.1f')

    print(f"{os.linesep}Maximum temperature change for {city_abv} during period specified is {temp_change}C.{os.linesep}")

    temp_dict = {
        "city": city,
        "date": date,
        "temp_change": float(temp_change),
    }
    with open(f"{jsonfilename}_temp.json", "w") as outfile:
        json.dump(temp_dict, outfile)
    
    return

def main():

    args = _get_args(sys.argv[1:])

    # The complete city name is required when constructing the dataframe.
    if args.city in "bos":
        city = "BOSTON, MA US"
    elif args.city in "mia":
        city = "MIAMI INTERNATIONAL AIRPORT, FL US"
    elif args.city in "jnu":
        city = "JUNEAU AIRPORT, AK US"
    else:
        print("invalid city")
        sys.exit()

    if args.function in "days-of-precip":
        days_of_precip(city, args.city)
    elif args.function in "max-temp-delta":
        max_temp_delta(city, args.city, args.month, args.year)
    else:
        print("Invalid Function")
        sys.exit()

if __name__ == "__main__":
   main()
