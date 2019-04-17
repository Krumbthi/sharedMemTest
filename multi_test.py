from multiprocessing import Manager, Process, Value, Array
import logging

# ----------------------------------------------------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------------------------------------------------
logging.basicConfig(format='%(asctime)s %(name)s %(message)s', level=logging.DEBUG)
Logger = logging.getLogger(__name__)


def worker(d, key, value):
    d[key] = value


def worker2(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]


if __name__ == '__main__':
    mgr = Manager()
    d = mgr.dict()
    jobs = [Process(target=worker, args=(d, i, i*2)) for i in range(10)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    
    Logger.debug('Results: %s' % d)

    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=worker2, args=(num, arr))
    p.start()
    p.join()

    Logger.debug(num.value)
    Logger.debug(arr[:])
