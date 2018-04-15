#!/user/bin/python3

def reduce(function, iterate, initializer=None):
    it = iter(iterate)
    if initializer is None:
        try:initializer = next(it)
        except StopIteration:raise TypeError('reduce() of empty sequence with no initial value')
    accumulate_value = initializer
    for x in it:accumulate_value = function(accumulate_value, x)
    return accumulate_value
