'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

import sqlite3 as sqlite
from powerbot.database.sql import database,create_state_change,create_reports,create_messages,create_tweets 


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

def insertStateChange():
    print 'inserting state change'

def insertDailyReport():
    print 'Inserting daily report'

def insertReport():
    print 'Inserting report'
            
def insertMessage():
    print 'Inserting message'

def insertTweetQueue():
    print 'Inserting in Tweet queue'
  