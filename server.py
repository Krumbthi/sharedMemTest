import json
import os
import sys
import logging
import time
import mmap
import subprocess
from random import sample

# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(name)s %(message)s', level=logging.DEBUG)
Logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------------------------------
# Defines
# ----------------------------------------------------------------------------------------------------------------------
ShmPath = "/dev/shm"
Rand = ["add", "sub", "mul", "div"]

# ----------------------------------------------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# main loop
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # create file first
    fn = os.path.normpath(ShmPath + '/' + 'suchfoo')
    d = {"cnt": 0, "msg": "Hello World"}
    
    # write a simple example file
    Logger.debug("create: {}".format(fn))
    
    f = open(fn, "w")
    f.write(json.dumps(d))
    f.close()
    Logger.debug("Writing to file")

    # fi = open(fn, 'r+')
    # mm = mmap.mmap(fi.fileno(), 0, access=mmap.ACCESS_WRITE)
    # Logger.debug("Writing to file")
    # mm.write(json.dumps(d))
    # mm.close()

    Running = True

    try:
        while Running:
            d["cnt"] += 1
            #d['msg'] = 'counter inc to: %d' %d['cnt']
            d["msg"] = sample(Rand, 1)[0]

            with open(fn, 'r+') as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
                Logger.debug("Writing to file")
                mm.write(json.dumps(d).encode())
                mm.close()

            time.sleep(1)

    except KeyboardInterrupt:
        Running = False
        os.system("rm {}".format(fn))

if __name__ == '__main__':
    main()