import datetime
import time
import logging
from powerbot.database.access import get_state_change_btw, new_report,\
    get_report, new_tweet
from powerbot.database.models import StateChange, Report, Tweet
from itertools import izip
import random

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

def sleep_till_midnight():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_time = time.mktime(tomorrow.timetuple()) + random.randrange(0,600)
    logging.info('Next report generation scheduled at ' + time.ctime(tomorrow_time))
    #time.sleep(int(tomorrow_time) - int(time.time()) )
    time.sleep(10)

def generate_reports():
    today = datetime.date(2012,12,12) #datetime.datetime.today()
    today_string = today.strftime('%m-%d-%w')
    month, day, weekday = (int(x) for x in today_string.split('-'))
    
    generate_daily_reports()
    
    if weekday == 0:
        generate_weekly_reports()
        
    if day == 1:
        generate_monthly_reports()
    
    if day == 1 and month%3 == 1:
        generate_quarterly_reports()
    
    if day == 1 and month == 1:
        generate_yearly_reports()
    
def generate_daily_reports():
    logging.info('Generating daily reports')
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    yesterday_start = int(time.mktime(yesterday.timetuple()))
    today_start = yesterday_start + 86400
    records = get_state_change_btw(yesterday_start, today_start)
    if records == None or len(records) == 0:
        logging.info('No records available to generate daily report')
        return
     
    if records[0].new_state == 0:
        if records[0].timestamp == yesterday_start:
            del records[0]
        else:
            first_on_record = StateChange(1, yesterday_start)
            records.insert(0, first_on_record)     
    
    if records[-1].new_state == 1:
        if records[-1].timestamp == today_start:
            del records[-1]
        else:
            last_off_record = StateChange(0, today_start)
            records.append(last_off_record)

    on_time = 0
    for x, y in pairwise(records):
        single_on_time = y.timestamp - x.timestamp
        on_time = on_time +  single_on_time
        logging.info("%s - %s = %ss" % (x, y, single_on_time))
    
    message = "Electricity ON TIME on %s is %s. i.e, %.2f%%" % (yesterday.strftime('%b %d, %Y'), datetime.timedelta(seconds=on_time),on_time/864.0)
    logging.info(message)
    new_tweet(Tweet(int(time.time()), message, None, today_start + 43200))
    new_report(Report(yesterday_start, on_time, ReportType.DAILY_REPORT))
    print get_report(yesterday_start, ReportType.DAILY_REPORT) 

def generate_weekly_reports():
    logging.info('Generating weekly reports')

def generate_monthly_reports():
    logging.info('Generating monthly reports')

def generate_quarterly_reports():
    logging.info('Generating quarterly reports')

def generate_yearly_reports():
    logging.info('Generating yearly reports')
    
class ReportType:
    DAILY_REPORT = 0
    WEEKLY_REPORT = 1
    MONTHLY_REPORT = 2
    QUARTERLY_REPORT = 3
    YEARLY_REPORT = 4
