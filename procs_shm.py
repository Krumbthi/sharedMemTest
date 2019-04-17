import os
import json
import multiprocessing
import mmap
import time


FILENAME = os.path.normpath("/dev/shm/sharedfile")


def init_file():
    os.system("touch %s" % FILENAME)
    with open(FILENAME, "w+b") as f:
        f.write(42*b'\0')


def print_cube(lock, num):
    d = {"msg": "", "value": 0}
    f = open(FILENAME, "r+b")
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)

    while True:
        lock.acquire()
        d["msg"] = "Cube"
        d["value"] = num*num*num
        print(json.dumps(d).encode())
        m.write(json.dumps(d).encode())
        
        lock.release()
        time.sleep(0.5)
    
    m.close()
            

def print_square(lock, num):
    d = {"msg": "", "value": 0}
    f = open(FILENAME, "r+b")
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
    
    while True:
        lock.acquire()
        d["msg"] = "Square"
        d["value"] = num*num
        m.write(json.dumps(d).encode())
        lock.release()
        time.sleep(0.5)

    m.close()


def reader_proc(lock):
    f = open(FILENAME, "r+b")
    m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    while True:
        lock.acquire()
        res = m.read()
        try:
            print(json.loads(res.decode()))
        except:
            lock.release()
            continue
        lock.release()
        time.sleep(1)
    m.close()

def main():
    lock = multiprocessing.Lock()
    init_file()

    p1 = multiprocessing.Process(target=print_cube, args=(lock, 5, ))
    p2 = multiprocessing.Process(target=print_square, args=(lock, 10, ))
    p3 = multiprocessing.Process(target=reader_proc, args=(lock,))
    
    try:
        p1.start()
        p2.start()
        p3.start()
    except KeyboardInterrupt:
        p1.join()
        p2.join()
        p3.join()

    # os.system("rm -r %s" % FILENAME)
    print("DONE")


if __name__ == "__main__":
    main()
