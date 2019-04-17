import json
import os
import sys
import logging
import asyncio
import time
import share


# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(name)s %(message)s', level=logging.DEBUG)
Logger = logging.getLogger(__name__)

Running = True


def main():
    # create file first
    # with open('/tmp/suchfoo', 'wb') as f:
    #     f.write(share.Foo(42, 98).as_bytes.encode())
    #
    # f = share.foo_from_mmap('/tmp/suchfoo')
    f = share.foo_from_shm('suchfoo')
    Logger.debug(f)


if __name__ == '__main__':
    main()