import time


def check(timeout, time_end):
    if time_end == 0:
        time_end = time.time() + float(timeout)
        lock = False
    else:
        print "Timer:Lock - Time left:"+str(time_end - time.time())
        if time.time() < time_end:
            lock = True
            # print "Timer:Locked"
        else:
            time_end = time.time() + float(timeout)
            lock = False
            # print "Timer:Unlocked"
    return (time_end, lock)
