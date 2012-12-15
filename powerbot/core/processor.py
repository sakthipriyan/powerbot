'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

from powerbot.core.sensor import get_status
import time
import threading
from powerbot.database.models import StateChange, Tweet
from powerbot.database import access

old_status = True

def doSensing():
    while(True):
        new_status = get_status()
        global old_status
        if(new_status != old_status):
            print str(time.asctime()) + ' Status changed from ' + str(old_status) + ' to '  + str(new_status)
            old_status = new_status
            processChange(StateChange(1 if new_status else 0, int(time.time())))
        time.sleep(1)

def processChange(stateChange):
    access.insertStateChange(stateChange)
    message = access.selectMessage(stateChange)
    tweet = Tweet(stateChange.timestamp, message.message, None, stateChange.timestamp + 600)
    access.insertTweet(tweet)

def background():
    print "Generates reports"

def main():
    print 'Starting service'
    senseThread = threading.Thread(target = doSensing)
    processThread = threading.Thread(target = background)
    senseThread.start()
    processThread.start()
    
if __name__ == "__main__":
    main()