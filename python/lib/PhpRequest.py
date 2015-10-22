import os
import threading
import time
"""
Web Request
"""

def send_data(data, path, timestamp, state):
    if(state):
        cmd = "/usr/bin/php-cgi "+path+"/data.php data="+data.encode("utf8")+" time="+str(timestamp)+" state="+state.encode("utf8")
    else:
        # Execute every action related to this trigger
        cmd = "/usr/bin/php-cgi "+path+"/data.php data="+data.encode("utf8")+" time="+str(timestamp)
    print "command"+str(cmd)
    os.system(cmd)


def send(path, data, state=False):
    timestamp = int(time.time())
    sending_thread = threading.Thread(target=send_data, args=(data, path, timestamp, state))
    sending_thread.start()
