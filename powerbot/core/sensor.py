'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

'''
import RPi.GPIO as GPIO


def get_status():
    return not GPIO.input(4)
'''
import logging

def init_sensor():    
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(4, GPIO.IN)
    logging.info('Setting up sensor')
    
import time, random
status = True
next_change = 0

def get_status():
    #return not GPIO.input(4)
    
    #TODO - remove this once 
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