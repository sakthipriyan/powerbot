'''
Created on 15-Dec-2012

@author: sakthipriyan
'''
import time, random

status = True
next_change = 0


def get_status():
    global status
    if(change_input()):
        status = not status
    return status

def change_input():
    global next_change
    current_time = int(time.time())
    if(next_change < current_time):
        random_time = random.randrange(10,30,5)
        next_change = current_time + random_time
        return True
    else:
        return False    