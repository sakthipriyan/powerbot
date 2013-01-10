'''
This file contains SQL strings
'''
from powerbot.core.config import database_file
database = database_file

##Core table where status change is recorded##
create_state_change = '''CREATE TABLE "state_change" (
    "timestamp" INTEGER PRIMARY KEY NOT NULL,
    "new_state" INTEGER NOT NULL
);'''
#Consolidated reports table
create_reports = '''CREATE TABLE "reports" (
    "date" INTEGER NOT NULL,
    "report_type" INTEGER NOT NULL,
    "on_time" INTEGER NOT NULL,
    PRIMARY KEY (date, report_type)
);'''
#messages table
create_messages = '''CREATE TABLE "messages" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "new_state" INTEGER NOT NULL,
    "message" TEXT NOT NULL,
    "usage" INTEGER NOT NULL DEFAULT (0)
)'''
#used in case of Internet connectivity problem 
create_tweets = '''CREATE TABLE "tweets" (
    "timestamp" INTEGER PRIMARY KEY NOT NULL,
    "message" TEXT NOT NULL,
    "picture" TEXT,
    "expires" INTEGER NOT NULL
);'''

insert_state_change = 'INSERT INTO state_change values(?,?)'
select_last_state_change = 'SELECT * FROM state_change ORDER BY timestamp DESC LIMIT 1'
select_state_change_btw = 'SELECT * FROM state_change WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp'

insert_report = 'INSERT INTO reports values(?,?,?)'
select_report = 'SELECT * FROM reports WHERE date = ? AND report_type = ?'
select_reports_btw = 'SELECT * FROM reports WHERE report_type = ? AND date BETWEEN ? AND ? ORDER BY date'

insert_tweet = 'INSERT INTO tweets values(?,?,?,?)'
select_tweet = 'SELECT * FROM tweets where expires > ? ORDER BY timestamp LIMIT 1'
update_tweet_posted = 'UPDATE tweets set expires = ? where timestamp = ?'
delete_tweets = 'DELETE FROM tweets where timestamp < ?'

insert_message = 'INSERT INTO messages("new_state","message") values (?,?)'
select_message = 'SELECT * FROM messages where new_state=? ORDER BY usage LIMIT 1'
update_message_usage = 'UPDATE messages set usage = usage + 1 where id = ?'
remove_message = 'DELETE FROM messages where id = ?'
