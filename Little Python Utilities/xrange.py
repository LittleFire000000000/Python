#!/usr/bin/python3
__author__ = 'Aidan'


class XRange:
    def __init__(self, *a):
        self.start = 0
        self.stop = 0
        self.step = 0
        if len(a) == 1:
            self.stop = a[0]
            self.start = 0
            self.step = 1
        elif len(a) == 2:
            self.start = a[0]
            self.stop = a[1]
            self.step = 1
        elif len(a) == 3:
            self.start = a[0]
            self.stop = a[1]
            self.step = a[2]
        self.step = abs(float(repr(self.step)))

    def __iter__(self):
        if self.stop > self.start:
            itr = self.start - self.step
            while itr < self.stop:
                itr += self.step
                yield itr
        elif self.start > self.stop:
            itr = self.start + self.step
            while itr > self.stop:
                itr -= self.step
                yield itr
        else:
            return []
