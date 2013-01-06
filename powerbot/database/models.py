'''
Created on 15-Dec-2012
@author: sakthipriyan
'''
import datetime

class StateChange(object):
    def __init__(self, new_state, timestamp):
        self.new_state = new_state
        self.timestamp = timestamp
    def __str__(self):
        status = 'ON' if self.new_state else 'OFF'
        return 'StateChange[timestamp=' + str(datetime.datetime.fromtimestamp(self.timestamp)) + ',status=' + status + ']' 

class Report(object):
    def __init__(self, date, on_time, report_type):
        self.date = date  
        self.report_type = report_type
        self.on_time = on_time
    def __str__(self):
        return 'Report[date=' + str(datetime.datetime.fromtimestamp(self.date).strftime('%Y-%m-%d')) + ',report_type=' + str(self.report_type) + ', on_time=' + str(self.on_time) + ']'

class Message(object):
    def __init__(self, message_id, new_state, message, usage):
        self.id = message_id
        self.new_state = new_state
        self.message = message
        self.usage = usage
    def __str__(self):
        return 'Message[id=' + str(self.id) + ',new_state=' + str(self.new_state) + ',message=' + str(self.message) + ',usage=' + str(self.usage) + ']'

class Tweet(object):
    def __init__(self, timestamp, message, picture, expires):
        self.timestamp = timestamp
        self.message = message
        self.picture = picture
        self.expires = expires
    def __str__(self):
        return 'Tweet[timestamp=' + str(datetime.datetime.fromtimestamp(self.timestamp)) + ',message=' + str(self.message) + ',picture=' + str(self.picture) + ',expires=' + str(datetime.datetime.fromtimestamp(self.expires)) + ']'
        
