'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

import sqlite3 as sqlite
from powerbot.database.sql import database,create_state_change,create_reports,create_messages,create_tweets ,\
    insert_state_change, select_message, update_message_usage, insert_tweet,\
    insert_message, insert_report
from powerbot.database.models import Message

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

def insertStateChange(stateChange):    
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

def insertReport(report):
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

def insertMessage(message):
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

def selectMessage(stateChange):
    connection = None
    message = None
    try:
        connection = sqlite.connect(database)
        cursor = connection.cursor()
        cursor.execute(select_message,(stateChange.new_state,))
        data = cursor.fetchone()
        message = Message(data[0], data[1], data[2], data[3])
        cursor.execute(update_message_usage,(message.id,))
        connection.commit()
    except sqlite.Error, e:
        print "Error %s:" % e.args[0]
    finally:
        if connection:
            connection.close()
    return message

def insertTweet(tweet):
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
