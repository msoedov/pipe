from unpyc import decompile
from functools import reduce


def val(_pipe):
    return _pipe.val


value = val


def star(fn):
    return lambda a: fn(*a)


def partial(t):
    def transformation(fn, pairwise=False, *a, **kw):
        def _(seq):
            _.lmbda = fn
            if pairwise:
                nonlocal fn
                fn = star(fn)
            try:
                return t(fn, seq, *a, **kw)
            except:
                raise
        return _
    return transformation


class _Enum(object):
    """
    >>> pipe([1, 2, 3, 3, 9]) \
        >> Enum.map(lambda x: x * 2) \
        >> Enum.filter(lambda x: x % 3) \
        >> Enum.into(set) \
        >> Enum.get
    {2, 4}

    >>> pipe({'a': 1, 'b': 2, 'c': 12}) \
        >> Enum.into(dict.items) \
        >> Enum.filter(lambda k, v : v > 1.5, pairwise=True) \
        >> Enum.into(dict) \
        >> Enum.get
    {'b': 2, 'c': 12}
    """


def into(new_type):
    def receiver(seq_or_val):
        return new_type(seq_or_val)
    return receiver

Enum = _Enum()
Enum.map = partial(map)
Enum.filter = partial(filter)
Enum.reduce = partial(reduce)
Enum.sum = partial(sum)
Enum.into = into
Enum.get = val


class pipe(object):
    """
    """

    def __init__(self, val):
        self.val = val
        self.p = None
        self.r = None
        self.steps = 0

    def transform(self, transformation):
        if transformation is val:
            return self.val
        trapped = None
        try:
            r = self.val
            self.val = transformation(self.val)
            self.p = transformation
            self.steps += 1
        except Exception as e:
            trapped = e
        if trapped:
            code = decompile(self.p.lmbda)
            msg = 'Failied to apply: {code} To {seq} on step {step}\n Previous step {prev}'.format(code=code, seq=self.val, prev=self.r, step=self.steps)
            raise type(trapped)(msg)
        self.r = r
        return self

    def __repr__(self):
        return '>> {}'.format(self.val)

    __rshift__ = transform
