'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

from powerbot.core.sensor import get_status
import time
import threading
from powerbot.database.models import StateChange, Tweet
from powerbot.database import access
import datetime
from powerbot.core.tweet import post_tweet

old_status = True

def do_sensing():
    while(True):
        new_status = get_status()
        global old_status
        if(new_status != old_status):
            print str(time.asctime()) + ' Status changed from ' + str(old_status) + ' to '  + str(new_status)
            old_status = new_status
            process_change(StateChange(1 if new_status else 0, int(time.time())))
        time.sleep(1)

def process_change(stateChange):
    access.new_state_change(stateChange)
    message = access.get_message(stateChange)
    flag =  'ON' if stateChange.new_state else 'OFF'
    sign =  datetime.datetime.fromtimestamp(stateChange.timestamp).strftime("  ~ %H:%M "+flag)
    tweet = Tweet(stateChange.timestamp, message.message + sign, None, stateChange.timestamp + 600)
    access.new_tweet(tweet)
    post_tweet(tweet.message)

def background():
    print "Generates reports"

def main():
    print 'Starting service'
    senseThread = threading.Thread(target = do_sensing)
    processThread = threading.Thread(target = background)
    senseThread.start()
    processThread.start()
    
if __name__ == "__main__":
    main()