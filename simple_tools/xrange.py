#!/usr/bin/python3


class XRange :
    """ Better than range(). """
    
    start: float
    stop: float
    step: float
    inclusive: bool
    
    def __init__(self, *start_stop_step, inclusive_end: bool = True) :
        self.start = 0
        self.stop = 0
        self.step = 0
        #
        if len(start_stop_step) == 1 :
            self.start = 0
            self.stop = start_stop_step[0]
            self.step = 1
        elif len(start_stop_step) == 2 :
            self.start = start_stop_step[0]
            self.stop = start_stop_step[1]
            self.step = 1
        elif len(start_stop_step) == 3 :
            self.start = start_stop_step[0]
            self.stop = start_stop_step[1]
            self.step = start_stop_step[2]
        #
        self.step = abs(float(repr(self.step)))
        self.inclusive = inclusive_end
    
    def __iter__(self) :
        if self.stop > self.start :
            itr = self.start
            while itr <= self.stop if self.inclusive else itr < self.stop :
                yield itr
                itr += self.step
        elif self.start > self.stop :
            itr = self.start
            while itr >= self.stop if self.inclusive else itr > self.stop :
                yield itr
                itr -= self.step
        else :
            yield from [self.start] if self.inclusive else []
