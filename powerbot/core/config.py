'''
Created on 19-Dec-2012

@author: sakthipriyan
'''

#TODO - update with your twitter tokens
twitter_token = 'Insert your twitter token here'
twitter_secret = 'Insert your twitter secret here'
oauth_token = 'Insert your oauth token here'
oauth_token_secret = 'Insert your oauth token secret here'

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
