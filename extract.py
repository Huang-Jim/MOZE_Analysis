"""
@author: jim
"""
import argparse
from collections import OrderedDict

import pandas as pd
import joblib

from structures import MonthSheet
from utils import duration_args

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--duration', default='all')

if __name__ == '__main__':
    data_path = './MOZE.csv'
    data = pd.read_csv(data_path)
    args = parser.parse_args()
    duration = args.duration

    DATES = duration_args(data['日期'], duration)

    month_sheets = {}

    for input_idx, date in enumerate(DATES):
        focus_data = data[['類型', '主類別', '子類別', '日期', '金額']]
        month_data = focus_data.loc[focus_data['日期'].str.match(date)]

        month_sheet = MonthSheet(date)
        for index, row in month_data.iterrows():
            month_sheet.add_row(row=row)

        month_sheets[date] = month_sheet

    month_sheets = OrderedDict(sorted(month_sheets.items(), key=lambda x: x[0]))
    joblib.dump(month_sheets, './month_sheets.pkl')
    # https://stackoverflow.com/questions/49621169/joblib-load-main-attributeerror

    print()
