import os
import multiprocessing
import mmap


fn = os.path.normpath("/dev/shm/sharedfile")


def init_file():
    os.system("touch %s" % fn)
    with open(fn, "r+") as f:
        f.write("This is the init of the file")


def print_cube(num):
    with open(fn, 'r+') as f:
        with mmap.mmap(f.fileno(), 0) as m:
            s = "Cube: {}".format(num*num*num)
            m.write(s.encode())
            m.close()
            print(s)


def print_square(num):
    with open(fn, 'r+') as f:
        with mmap.mmap(f.fileno(), 0) as m:
            s = "Square: %d" % (num*num)
            m.write(s.encode())
            m.close()
            print(s)


def main():
    init_file()

    p1 = multiprocessing.Process(target=print_cube, args=(10, ))
    p2 = multiprocessing.Process(target=print_square, args=(10, ))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    with open(fn, 'r') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as m:
            res = m.read()
            m.close()
            print(res)

    print("DONE")


if __name__ == "__main__":
    main()