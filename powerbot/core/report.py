import datetime
import time
import logging

def get_next_schedule_time():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    delay = int(time.mktime(tomorrow.timetuple())) - int(time.time())
    return delay
     
def daily_processing():
    logging.info('TODO - Processing daily records')
    
def weekly_processing():
    logging.info('TODO - Processing weekly records')
    
def monthly_processing():
    logging.info('TODO - Processing monthly records')
    
def quarterly_processing():
    logging.info('TODO - Processing quarterly records')
    
def yearly_processing():
    logging.info('TODO - Processing yearly records')