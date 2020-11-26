from chinese_calendar import is_workday, is_holiday
from datetime import datetime, timedelta
import datetime

# Calculate the workdays between start and end.
def calculate_work_days(date_start, date_end):
    if type(date_start) == str:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d').date()
    if type(date_end) == str:
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    if date_start > date_end:
        date_start, date_end = date_end, date_start
    counts = 0
    while True:
        if date_start > date_end:
            break
        if is_workday(date_start):
            counts += 1
        date_start += timedelta(days=1)
    return counts


# Calculate the trade days between start and end.
def calculate_trade_days(date_start, date_end):
    if type(date_start) == str:
        date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d').date()
    if type(date_end) == str:
        date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d').date()
    if date_start > date_end:
        date_start, date_end = date_end, date_start

    counts = 0
    while True:
        if date_start > date_end:
            break
        if is_holiday(date_start) or date_start.weekday() == 5 or date_start.weekday() == 6:
            date_start += timedelta(days=1)
            continue
        counts += 1
        date_start += timedelta(days=1)
    return counts

def is_trade_day(date_str):
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    if is_holiday(date) or date.weekday() == 5 or date.weekday() == 6:
        return False
    return True

def add_day(date_str, days):
    cur_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    result_date = cur_date + datetime.timedelta(days=days)
    result_date = result_date.strftime("%Y-%m-%d")
    return result_date


def minus_day(date_str, days):
    cur_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    result_date = cur_date - datetime.timedelta(days=days)
    result_date = result_date.strftime("%Y-%m-%d")
    return result_date


def add_minutes(time_str, minutes):
    cur_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    result_time = cur_time + datetime.timedelta(minutes=minutes)
    result_time = result_time.strftime("%Y-%m-%d %H:%M")
    return result_time


def minus_minutes(time_str, minutes):
    cur_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M')
    result_time = cur_time - datetime.timedelta(minutes=minutes)
    result_time = result_time.strftime("%Y-%m-%d %H:%M")
    return result_time
