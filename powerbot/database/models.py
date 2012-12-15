'''
Created on 15-Dec-2012
@author: sakthipriyan
'''

import time

class StateChange(object):
    def __init__(self, new_state, timestamp = int(time.time())):
        self.new_state = new_state
        self.timestamp =  timestamp

class Report(object):
    def __init__(self, date, on_time, report_type = 0):
        self.date = date  
        self.report_type = report_type
        self.on_time = on_time
        
class Message(object):
    def __init__(self, message_id, new_state, message, usage = 0):
        self.id = message_id
        self.message = message
        self.new_state = new_state
        self.usage = usage
        
class Tweet(object):
    def __init__(self, message, picture, expires, timestamp = int(time.time())):
        self.message = message
        self.picture = picture
        self.expires = expires
        self.timestamp = timestamp