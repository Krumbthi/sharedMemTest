from libc.stdlib cimport malloc, free

from posix.mman cimport (
    mmap,
    shm_open,
    PROT_READ,
    PROT_WRITE,
    MAP_SHARED,
)

from posix.fcntl cimport (
    O_RDWR,
    O_CREAT
)

from posix.unistd cimport ftruncate

cdef struct foo:
    int bar
    int baz

cdef class Foo:
    cdef foo* _foo
    cdef bint free_on_dealloc

    def __init__(self, bar=0, baz=0):
        self._foo = <foo*>malloc(sizeof(foo))
        self.bar = bar
        self.baz = baz
        self.free_on_dealloc = True

    def __dealloc__(self):
        if self.free_on_dealloc:
            free(self._foo)

    @staticmethod
    cdef Foo from_foo(foo* the_foo):
        cdef Foo c = Foo()
        free(c._foo)
        c._foo = the_foo
        return c

    @property
    def bar(self):
        return self._foo[0].bar

    @bar.setter
    def bar(self, int val):
        self._foo[0].bar = val

    @property
    def baz(self):
        return self._foo[0].baz

    @baz.setter
    def baz(self, int val):
        self._foo[0].baz = val

    @property
    def as_bytes(self):
        return str((<char*>self._foo)[:sizeof(foo)])

    @classmethod
    def from_bytes(cls, bytes foo_bytes):
        return Foo.from_foo(<foo*>(<char*>foo_bytes))

    def __len__(self):
        return sizeof(foo)

    def __repr__(self):
        return self.__class__.__name__ + '({self.bar}, {self.baz})'.format(self=self)

def foo_from_mmap(file_name):
    with open(file_name, 'ra+b') as f:
        ret_foo = Foo.from_foo(<foo*>(mmap(
            NULL, sizeof(foo), PROT_READ|PROT_WRITE, MAP_SHARED, f.fileno(), 0)
        ))
        ret_foo.free_on_dealloc = False
        return ret_foo

def foo_from_shm(bytes tagname):
    cdef int fd
    fd = shm_open(<const char*>tagname, O_RDWR | O_CREAT, 0666)
    ftruncate(fd, sizeof(foo))
    ret_foo = Foo.from_foo(<foo*>(mmap(
        NULL, sizeof(foo), PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0)
    ))
    ret_foo.free_on_dealloc = False
    return ret_foo
