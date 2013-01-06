#!/usr/bin/python
# /etc/init.d/powerbot

'''
Created on 15-Dec-2012

@author: sakthipriyan
'''

import sys
from powerbot.core import processor
from powerbot.core.daemon import Daemon

if __name__ == '__main__':
    processor.main()
    
class MyDaemon(Daemon):
    def run(self):
        processor.main()    
'''
 
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/powerbot.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
        
'''