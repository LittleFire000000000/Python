#!/usr/bin/python3
from typing import \
    Iterable, \
    Tuple, \
    Union, \
    Callable


def switch_flat(*parameter_triplets: [object, Iterable[Union[object, Callable, Iterable]]],
                default: Tuple[Callable, Iterable] = None,
                error: Tuple[Callable, Iterable] = None) -> object :
    """
    Implement a switch structure from C/C++ into Python.
    The parameter_triplets is list or tuple starts with a first value called switch.
    After the switch follow one or more triplets of values.
    Each triplet has a case (possible value for switch), a function/callable (called on switch==case), and arguments (fxn(*arguments)).
    In other words, when a case matches (via ==) the switch, this function returns the correlating function call with the arguments distributed.
    After all cases are checked, regardless of whether any matches were found, the function returns the call of default[0](default[1]).
    This a called the default case or base case.
    The error argument is new and Python-specific addition to this edition of the switch structure.
    If parameter_triplets is empty, the base case is invoked (if given) and then the error is called (error[0](*error[1])), if given.
    If neither forms ([switch, *[case, fxn, args]] or []) apply, a ValueError is raised.
    :param parameter_triplets: [switch, *[case, fxn, args]] or []
    :param default: None or [fxn, args]
    :param error: None or [fxn, args]
    :return: None or object
    """
    length: int = len(parameter_triplets)
    if (length - 1) % 3 == 0 :  # check if a [switch, *[case, fxn, args]] was given
        for n, b in enumerate(parameter_triplets) :
            if (n - 1) % 3 == 0 :
                if parameter_triplets[0] == parameter_triplets[n] :
                    try :
                        return parameter_triplets[n + 1](*parameter_triplets[n + 2])
                    except TypeError :
                        try :
                            return parameter_triplets[n + 1]()
                        except TypeError :
                            return parameter_triplets[n + 1]
    elif length == 0 :  # []
        pass
    else :  # invalid command
        raise ValueError
    if default is not None :
        return default[0](*default[1])
    elif error is not None :
        return error[0](*error[1])
    else :
        return None


def switch(*parameter_triplets: [object, [[object, Callable, Iterable]]],
           default: Tuple[Callable, Iterable] = None,
           error: Tuple[Callable, Iterable] = None) -> object :
    """ Invoke simple_flat(). """
    
    def convert() :
        nonlocal parameter_triplets
        parameter_triplets_iterator: iter = iter(parameter_triplets)
        yield next(parameter_triplets_iterator)  # switch
        for case, fxn, args in parameter_triplets_iterator :
            yield case
            yield fxn
            yield args
    
    return switch_flat(*convert(), default=default, error=error)


def test_switch_flat_print(*s: [int], default: bool = True, error: bool = True) :
    assert len(s) < 2
    
    p: Callable[Iterable[str]] = lambda *st : st
    
    def printer(*args: [str, int]) -> int :
        print(*args)
        return args[1]
    
    a: [] = list(s) + \
            [
                0, printer, ['Zero', 0],
                1, printer, ['One', 1],
                2, printer, ['Two', 2],
                3, printer, ['Three', 3]
            ] if len(s) == 1 else []
    return switch_flat(*a, default=(p, ('Default',)) if default else None, error=(p, ('Error',)) if error else None)


def test_switch_print(*s: [int], default: bool = True, error: bool = True) :
    assert len(s) < 2
    
    p: Callable[Iterable[str]] = lambda *st : st
    
    def printer(*args: [str, int]) -> int :
        print(*args)
        return args[1]
    
    a: [] = list(s) + \
            [
                (0, printer, ['Zero', 0]),
                (1, printer, ['One', 1]),
                (2, printer, ['Two', 2]),
                (3, printer, ['Three', 3])
            ] if len(s) == 1 else []
    return switch(*a, default=(p, ('Default',)) if default else None, error=(p, ('Error',)) if error else None)


def test_switch() :
    try :
        print('Testing flat')
        print('Test 1.1 returned ', test_switch_flat_print(), '.', sep='')
        print('Test 1.2 returned ', test_switch_flat_print(1), '.', sep='')
        print('Test 1.3 returned ', test_switch_flat_print(2), '.', sep='')
        print('Test 1.4 returned ', test_switch_flat_print(3), '.', sep='')
        print('Test 1.5 returned ', test_switch_flat_print(4), '.', sep='')
        print('Test 1.e returned ', test_switch_flat_print(4), '.', sep='')
        print('Test 1.d returned ', test_switch_flat_print(4, default=False), '.', sep='')
        print('Test 1.b returned ', test_switch_flat_print(4, error=False), '.', sep='')
        print('Test 1.r returned ', test_switch_flat_print(4, default=False, error=False), '.', sep='')
    except Exception as e :
        print('Error 1', e)
    try :
        print('Testing grouped')
        print('Test 2.1 returned ', test_switch_print(), '.', sep='')
        print('Test 2.2 returned ', test_switch_print(1), '.', sep='')
        print('Test 2.3 returned ', test_switch_print(2), '.', sep='')
        print('Test 2.4 returned ', test_switch_print(3), '.', sep='')
        print('Test 2.5 returned ', test_switch_print(4), '.', sep='')
        print('Test 2.e returned ', test_switch_print(4), '.', sep='')
        print('Test 2.d returned ', test_switch_print(4, default=False), '.', sep='')
        print('Test 2.b returned ', test_switch_print(4, error=False), '.', sep='')
        print('Test 2.r returned ', test_switch_print(4, default=False, error=False), '.', sep='')
    except Exception as e :
        print('Error 2', e)
    print('Done')


if __name__ == '__main__' :
    test_switch()
