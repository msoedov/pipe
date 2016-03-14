from functools import reduce


def val(_pipe):
    return _pipe.val


value = val


class pipe(object):
    """

    >>> pipe(6) \
        >> (lambda x: x + 1) \
        >> val
    7

    >>> pipe([1, 2, 3, 4, 6]) \
        >> filter(lambda x: x % 2 == 0) \
        >> map(lambda x: x ** 2) \
        >> map(lambda x: x % 10) \
        >> sum \
        >> value
    16

    >>> pipe([1, 2, 3, 4, 5]) \
        >> map(lambda x: x + 12) \
        >> reduce(lambda x, a: a * x,  1) \
        >> value
    742560
    """

    def __init__(self, val):
        self.val = val

    def transform(self, transformation):
        if transformation is val:
            return self.val
        self.val = transformation(self.val)
        return self

    __rshift__ = transform


oldfilter = filter
oldmap = map
oldreduce = reduce


def filter(fn):
    def closure(seq):
        return oldfilter(fn, seq)

    return closure


def map(fn):
    def closure(seq):
        return oldmap(fn, seq)

    return closure


def reduce(fn, initial=None):
    def closure(seq):
        return oldreduce(fn, seq, initial)

    return closure
