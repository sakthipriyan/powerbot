import sys
from powerbot.core.daemon import Daemon
from powerbot.core import processor
from powerbot.core.config import pid, out_file, err_file


class PowerbotDaemon(Daemon):
    def run(self):
        processor.service()

if __name__ == "__main__":
    daemon = PowerbotDaemon(pid,stdout=out_file,stderr=err_file)
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