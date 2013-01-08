import datetime
import time
import logging
from powerbot.database.access import get_state_change_btw

def sleep_till_midnight():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_time = time.mktime(tomorrow.timetuple())
    logging.info('Next report generation scheduled at ' + time.ctime(tomorrow_time))
    #time.sleep(int(tomorrow_time) - int(time.time()))
    time.sleep(100)

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
    yesterday_start = time.mktime(yesterday.timetuple())
    yesterday_end = yesterday_start + 86399
    records = get_state_change_btw(yesterday_start, yesterday_end)
    if records == None:
        logging.info('No records available to generate daily report')
        return
    

def generate_weekly_reports():
    logging.info('Generating weekly reports')

def generate_monthly_reports():
    logging.info('Generating monthly reports')

def generate_quarterly_reports():
    logging.info('Generating quarterly reports')

def generate_yearly_reports():
    logging.info('Generating yearly reports')