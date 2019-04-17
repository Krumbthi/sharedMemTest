import json
import os
import sys
import logging
import time
from enum import Enum
#import share


# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(name)s %(message)s', level=logging.DEBUG)
Logger = logging.getLogger("client")


# ----------------------------------------------------------------------------------------------------------------------
# Defines
# ----------------------------------------------------------------------------------------------------------------------
ShmPath = "/dev/shm"
class Action(Enum):
    ADD = 'add'
    SUB = 'sub'
    MUL = 'mul'
    DIV = 'div'

# ----------------------------------------------------------------------------------------------------------------------
# functions
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# main loop
# ----------------------------------------------------------------------------------------------------------------------
def main():
    # create file first
    fn = os.path.normpath(ShmPath + '/' + 'suchfoo')
    Running = True
    _file = open(fn, 'r')

    try:
        while Running:
            with open(fn, 'r+') as f:
                res = f.read()
                Logger.debug(res)
                if len(res) > 0:
                    #d = json.loads(res.decode())
                    d = json.loads(res)
                
                    if d['msg'] == "add":
                        d['cnt'] += 1
                    elif d['msg'] == "sub":
                        d['cnt'] -= 1
                    elif d['msg'] == "mul":
                        d['cnt'] *= 2
                    elif d['msg'] == "div":
                        d['cnt'] /= 2
                    
                    f.write(json.dumps(d))
                    Logger.debug(d["cnt"])

            time.sleep(0.2)

    except KeyboardInterrupt:
        Running = False
        # os.system("rm {}".format(fn))


if __name__ == '__main__':
    main()