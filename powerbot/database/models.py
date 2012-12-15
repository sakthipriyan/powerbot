'''
Created on 15-Dec-2012
@author: sakthipriyan
'''

class StateChange(object):
    def __init__(self, new_state, timestamp):
        self.new_state = new_state
        self.timestamp = timestamp
    def __str__(self):
        return str(self.timestamp) + ' ' + str(self.new_state) 

class Report(object):
    def __init__(self, date, on_time, report_type):
        self.date = date  
        self.report_type = report_type
        self.on_time = on_time
        
class Message(object):
    def __init__(self, message_id, new_state, message, usage):
        self.id = message_id
        self.new_state = new_state
        self.message = message
        self.usage = usage
        
class Tweet(object):
    def __init__(self, timestamp, message, picture, expires):
        self.timestamp = timestamp
        self.message = message
        self.picture = picture
        self.expires = expires 