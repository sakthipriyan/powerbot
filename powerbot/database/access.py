'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

import sqlite3 as sqlite
from powerbot.database.sql import database,create_state_change,create_reports,create_messages,create_tweets ,\
    insert_state_change, select_message, update_message_usage, insert_tweet,\
    insert_message, insert_report, select_tweet, delete_tweets
from powerbot.database.models import Message, Tweet
import time

def create_database():
    con = None
    try:
        con = sqlite.connect(database)
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print "SQLite version: %s" % data
        cur.execute(create_state_change)
        cur.execute(create_reports)
        cur.execute(create_messages) 
        cur.execute(create_tweets)
        print 'Tables created successfully'
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if con:
            con.close()

def init_database():
    new_message(Message(0,0,'Power gone again!!',0))
    new_message(Message(0,1,'And power came back again!!',0))
    new_message(Message(0,0,'No one knows when electricity will go!! It has gone now :(',0))
    new_message(Message(0,1,'Ha ha it came back! As always electricity shows up some time here',0))
    new_message(Message(0,0,'Now we are back to stone age!!',0))
    new_message(Message(0,1,'Back from past! Fans are running now, really!',0))
    new_message(Message(0,0,'When you desperately need electricity, you cannot find it!!',0))
    new_message(Message(0,1,'So, one more time it came back!!',0))


def new_state_change(stateChange):    
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_state_change, (stateChange.timestamp, stateChange.new_state))
        print 'Inserted state change record ' + str(stateChange)
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()

def new_report(report):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_report,(report.date, report.report_type, report.on_time))
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()

def new_message(message):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_message,(message.new_state,message.message))
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()

def get_message(stateChange):
    connection = None
    message = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(select_message,(stateChange.new_state,))
        data = cursor.fetchone()
        if(data):
            message = Message(data[0], data[1], data[2], data[3])
            cursor.execute(update_message_usage,(message.id,))
            connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()
    return message

def new_tweet(tweet):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_tweet,(tweet.timestamp,tweet.message,tweet.picture,tweet.expires))
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()

def next_tweet():
    connection = None
    tweet = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(select_tweet,(int(time.time()),))
        data = cursor.fetchone()
        tweet = Tweet(data[0], data[1], data[2], data[3])
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()
    return tweet

def remove_tweets(tweet):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(delete_tweets,(tweet.timestamp,))
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()