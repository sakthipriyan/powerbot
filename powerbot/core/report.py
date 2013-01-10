import datetime, time, logging, random

from powerbot.database.access import get_state_change_btw, new_report,\
    get_report, new_tweet, get_reports
from powerbot.database.models import StateChange, Report, Tweet
from itertools import izip

today = None
yesterday = None
today_start = 0
yesterday_start = 0

def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)

def sleep_till_midnight():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_time = time.mktime(tomorrow.timetuple()) + random.randrange(0,600)
    logging.info('Next report generation scheduled at ' + time.ctime(tomorrow_time))
    time.sleep(tomorrow_time - time.time())

def generate_reports():
    global today, today_start, yesterday, yesterday_start
    today = datetime.datetime(2014,1,1) #datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    yesterday_start = int(time.mktime(yesterday.timetuple()))
    today_start = yesterday_start + 86400
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
    records = get_state_change_btw(yesterday_start, today_start)
    if records == None or len(records) == 0:
        logging.info('No records available to generate daily report')
        return
    else:
        logging.info('Generating daily report')
         
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
    
    last_report = get_report(yesterday_start - 86400, ReportType.DAILY_REPORT)
    message = get_report_message(ReportType.DAILY_REPORT, on_time, yesterday)
    message += get_percentage_change(on_time, last_report.on_time if last_report else None)
    new_tweet(Tweet(int(time.time()), message, None, today_start + 43200))
    new_report(Report(yesterday_start, on_time, ReportType.DAILY_REPORT))

def generate_report(report_type, report_str, process_report, get_start_date):
    date = get_start_date()
    date_start = int(time.mktime(date.timetuple()))
    reports = get_reports(process_report, date_start, yesterday_start)
    
    if reports == None or len(reports) == 0:
        logging.info('No records available to generate ' + report_str + ' report')
        return    
    else:
        logging.info('Generating ' + report_str + ' report')

    on_time = 0 
    for report in reports:
        on_time = on_time + report.on_time
    avg_on_time = on_time/len(reports)
    
    last_report = get_report(date_start, report_type)
    message = get_report_message(report_type, avg_on_time, date, yesterday)    
    message += get_percentage_change(avg_on_time, last_report.on_time if last_report else None)
    
    new_tweet(Tweet(int(time.time()), message, None, today_start + 86400))
    new_report(Report(today_start, avg_on_time, report_type))    

def generate_weekly_reports():
    generate_report(ReportType.WEEKLY_REPORT, 'weekly', ReportType.DAILY_REPORT, get_last_week)

def generate_monthly_reports():
    generate_report(ReportType.MONTHLY_REPORT, 'monthly', ReportType.DAILY_REPORT, get_last_month)
    
def generate_quarterly_reports():
    generate_report(ReportType.QUARTERLY_REPORT, 'quarterly', ReportType.DAILY_REPORT, get_last_quarter)
        
def generate_yearly_reports():
    generate_report(ReportType.YEARLY_REPORT, 'yearly', ReportType.DAILY_REPORT, get_last_year)
    
def get_last_year():
    return datetime.date(today.year-1,today.month,today.day)    

def get_last_quarter():
    last_day = today.day
    last_month = today.month - 3
    last_year = today.year
    
    if last_month <= 0:
        last_month += 12
        last_year = today.year - 1
                
    return datetime.date(last_year,last_month,last_day)

def get_last_month():
    last_day = today.day
    last_month = today.month - 1 
    last_year = today.year
    
    if last_month is 0:
        last_month = 12
        last_year = today.year - 1        
    return datetime.date(last_year,last_month,last_day)

def get_last_week():
    return today + datetime.timedelta(days=-7)

def get_report_message(report_type,avg_on_time,from_date,to_date=None):
    if report_type is ReportType.DAILY_REPORT:
        return "Daily Report:%s. OFF TIME: %s. " % (from_date.strftime('%b %d, %Y'), datetime.timedelta(seconds=86400-avg_on_time))
    elif report_type is ReportType.WEEKLY_REPORT:
        return "Weekly Report:%s to %s. Average OFF TIME: %s. " % (from_date.strftime('%b %d, %Y'), to_date.strftime('%b %d, %Y'), datetime.timedelta(seconds=86400-avg_on_time))
    elif report_type is ReportType.MONTHLY_REPORT:
        return "Monthly Report:%s to %s. Average OFF TIME: %s. " % (from_date.strftime('%b %d, %Y'), to_date.strftime('%b %d, %Y'), datetime.timedelta(seconds=86400-avg_on_time))
    elif report_type is ReportType.QUARTERLY_REPORT:
        return "Quarterly Report:%s to %s. Average OFF TIME: %s. " % (from_date.strftime('%b %d, %Y'), to_date.strftime('%b %d, %Y'), datetime.timedelta(seconds=86400-avg_on_time))
    else:
        return "Yearly Report:%s to %s. Average OFF TIME: %s. " % (from_date.strftime('%b %d, %Y'), to_date.strftime('%b %d, %Y'), datetime.timedelta(seconds=86400-avg_on_time))
    
def get_percentage_change(avg_on_time, last_avg_on_time=None):
    message = "Availability: %.2f%%. " % (avg_on_time/864.0)
    if last_avg_on_time is not None:
        change = (avg_on_time-last_avg_on_time)/864.0
        message +=  "Change: %+.2f%%." % (change)
    return message

class ReportType:
    DAILY_REPORT = 0
    WEEKLY_REPORT = 1
    MONTHLY_REPORT = 2
    QUARTERLY_REPORT = 3
    YEARLY_REPORT = 4