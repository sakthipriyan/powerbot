'''
Created on 15-Dec-2012
@author: sakthipriyan
'''

import sqlite3 as sqlite
from powerbot.database.sql import database,create_state_change,create_reports,create_messages,create_tweets ,\
    insert_state_change, select_message, update_message_usage, insert_tweet,\
    insert_message, insert_report, select_tweet, delete_tweets,\
    select_last_state_change, update_tweet_posted, select_state_change_btw,\
    select_report
from powerbot.database.models import Message, Tweet, StateChange, Report
import time
import os
import logging

def init_database():
    dbPath = os.getcwd() +'/' +database
    if(not os.path.exists(dbPath)):
        logging.info('Creating database: ' + database) 
        create_database()
        logging.info('Inserting status change messages')
        insert_messages()

def create_database():
    con = None
    try:
        con = sqlite.connect(database)
        cur = con.cursor()
        cur.execute(create_state_change)
        cur.execute(create_reports)
        cur.execute(create_messages) 
        cur.execute(create_tweets)
        logging.info('Tables created successfully')
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if con:
            con.close()

def insert_messages():
    new_message(Message(0,0,'Power gone again!!',0))
    new_message(Message(0,1,'And power came back again!!',0))
    new_message(Message(0,0,'No one knows when electricity will go!! It has gone now :(',0))
    new_message(Message(0,1,'Ha ha it came back! As always electricity shows up some time here',0))
    new_message(Message(0,0,'Now we are back to stone age!!',0))
    new_message(Message(0,1,'Back from past! Fans are running now, really!',0))
    new_message(Message(0,0,'When you desperately need electricity, you cannot find it!!',0))
    new_message(Message(0,1,'So, one more time it came back!!',0))
    new_message(Message(0,0,'With high economic growth and inefficient government, we have no other option',0))
    new_message(Message(0,1,'Some times, government do remind us that we have working power plants by providing electricity',0))
    new_message(Message(0,0,'No one is sure here, when electricity shortage of supply will be fulfilled',0))
    new_message(Message(0,1,'AFAIK, since 2007 we were hearing that electricity shortage will be resolved in few months.',0))
    

def new_state_change(stateChange):    
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_state_change, (stateChange.timestamp, stateChange.new_state))
        connection.commit()
        logging.info('Inserted ' + str(stateChange))
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()

def get_last_state_change():
    connection = None
    stateChange = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(select_last_state_change)
        data = cursor.fetchone()
        if data:
            stateChange = StateChange(data[1], data[0])
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()
    return stateChange
    
def get_state_change_btw(start, end):
    connection = None
    statechange = []
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        for data in cursor.execute(select_state_change_btw,(start,end)):
            statechange.append(StateChange(data[1], data[0]))
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()
    return statechange

def new_report(report):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_report,(report.date, report.report_type, report.on_time))
        connection.commit()
        logging.info('Inserted ' + str(report))
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()

def get_report(date,report_type):
    connection = None
    report = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(select_report,(date,report_type))
        data = cursor.fetchone()
        report = Report(data[0], data[1], data[2])
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()
    return report
    

def new_message(message):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(insert_message,(message.new_state,message.message))
        connection.commit()
        logging.info('Inserted ' + str(message))
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
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
        if data:
            message = Message(data[0], data[1], data[2], data[3])
            cursor.execute(update_message_usage,(message.id,))
            connection.commit()
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
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
        logging.info('Inserted ' + str(tweet))
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
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
        if data:
            tweet = Tweet(data[0], data[1], data[2], data[3])
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()
    return tweet

def update_posted_tweet(tweet):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(update_tweet_posted,(tweet.timestamp,tweet.timestamp))
        connection.commit()
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()

def remove_tweets(tweet):
    connection = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(delete_tweets,(tweet.timestamp,))
        connection.commit()
    except sqlite.Error, e:
        logging.error("Error %s:" % e.args[0])
    finally:
        if connection:
            connection.close()