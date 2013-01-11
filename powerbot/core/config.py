'''
Created on 19-Dec-2012

@author: sakthipriyan
'''

#Log files
log_file = '/var/log/powerbot/service.log'
out_file = '/var/log/powerbot/sysout.log'
err_file = '/var/log/powerbot/syserr.log'

#SQlite db file
database_file = '/var/opt/powerbot/database.db'

#Powerbot will send tweet if this file is available
tweet_file = '/var/opt/powerbot/tweet'

#Process id for self termination
pid = '/var/run/powerbot.pid'
