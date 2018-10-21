#!/usr/bin/python3
from typing import Iterable, Dict, Tuple, Union, Callable, Any


def switch_flat(
        *parameter_trios: [
            object,  # switch
            Iterable[  # list of cases
                Union[  # each item in the list
                    object,  # case
                    Union[  # pair or trio
                        Tuple[  # trio w/ fxn and args
                            Callable,  # fxn
                            Iterable  # args
                        ],
                        object  # pair w/ constant
                    ]
                ]
            ]
        ],

        default: Tuple[Callable, Iterable[object]] = None,
        error: Tuple[Callable, Iterable[object]] = None
) -> Any:
    """
    Implement a switch structure from C/C++ into Python.
    The parameter_trios is a list or tuple that starts with a first value called switch or switch value.
    -
    
    After the switch follows one or more trios and/or pairs of values.
    For each trio encountered:
        The trio has a
            case [case] (possible value for switch),
            a function/callable [fxn] (called on switch==case), and
            arguments [args] (fxn([*[*]]args)).
        In other words, when a case matches (via ==) the switch, this function returns the returned value of the
            correlating function call with the arguments distributed.
        If the arguments are a dictionary, the function is called double-distributed (fxn(**args)).
        Else, if the arguments are an iterable, the function is called single-distributed (fxn(*args)).
        Otherwise, the function is called with the single-argument passed (fxn(args)).
    The exception is when the argument after case, fxn, isn't callable:
        In the scenario, no args are passed at all and none (not even "None") should be given.
        The fxn itself, being some constant, is returned.
        The scenario is an encounter with a pair.
    -
    
    After all cases are checked, regardless of whether any matches were found, the function returns the call of
        default[0](default[1]).
    This a called the default case or base case.
    -
    
    The error argument is new and Python-specific addition to this edition of the switch structure.
    It is a default to the base case.
    -

    If parameter_trios is empty, the base case is invoked (if given) and then the error is called (error[0](*error[1])),
        if given.
    -
    
    If neither forms ([switch, *[case, fxn[, args]]] or []) apply, a ValueError is raised.
    -
    
    :param parameter_trios: [switch, *[case, fxn[, args]]] or [] in Iterable or Generator form
    :param default: None or [fxn, args]
    :param error: None or [fxn, args]
    :return: None or object
    """
    parameter_trios_iterable: iter = iter(parameter_trios)
    try:
        try:
            switch_value = next(parameter_trios_iterable)  # get the switch value
        except StopIteration:
            raise AssertionError  # parameters are blank
        # iterate over cases
        for case in parameter_trios_iterable:  # trio/pairs ahead
            fxn = next(parameter_trios_iterable)  # get fxn
            is_callable = isinstance(fxn, Callable)  # function (trio) or constant (pair)
            # compare
            if switch_value == case:  # match
                if is_callable:  # function
                    args = next(parameter_trios_iterable)  # arguments
                    if isinstance(args, Dict):  # dictionary
                        return fxn(**args)
                    elif isinstance(args, Iterable):  # other iterable
                        return fxn(*args)
                    else:  # single constant
                        return fxn(args)
                else:  # constant
                    return fxn
            else:  # mismatch
                if is_callable:  # function (trio)
                    next(parameter_trios_iterable)  # gloss over arguments
    except AssertionError:  # blank parameters
        pass
    except StopIteration:  # invalid length
        raise ValueError
    # base case
    if default is not None:
        return default[0](*default[1])
    elif error is not None:
        return error[0](*error[1])
    else:
        return None


def switch(
        *parameter_trios: [
            object,  # switch
            Iterable[  # list of cases
                Iterable[  # each case in the list
                    Union[  # each item in the case
                        object,  # case
                        Union[  # pair or trio
                            Tuple[  # trio w/ fxn and args
                                Callable,  # fxn
                                Iterable  # args
                            ],
                            object  # pair w/ constant
                        ]
                    ]
                ]
            ]
        ],

        default: Tuple[Callable, Iterable[object]] = None,
        error: Tuple[Callable, Iterable[object]] = None
) -> Any:
    """ Invoke simple_flat(). """

    def convert():
        nonlocal parameter_trios
        parameter_trios_iterator: iter = iter(parameter_trios)
        yield next(parameter_trios_iterator)  # switch
        for trio_or_pair in parameter_trios_iterator:
            yield trio_or_pair[0]  # case
            fxn: Callable = trio_or_pair[1]  # function
            yield fxn
            if isinstance(fxn, Callable):
                yield trio_or_pair[2]  # args

    return switch_flat(*convert(), default = default, error = error)


class SwitchTests:  # namespace
    @staticmethod
    def test1_switch_flat_print(*s: [int], default: bool = True, error: bool = True):
        assert len(s) < 2

        p: Callable[[Tuple], Iterable[str]] = lambda *st: st

        def printer(*args: [str, int]) -> int:
            print(*args)
            return args[1]

        a: [] = \
            list(s) + [
                0, printer, ['Zero', 0],
                1, printer, ['One', 1],
                2, printer, ['Two', 2],
                3, printer, ['Three', 3]
            ] if len(s) == 1 else []
        return switch_flat(
            *a,
            default = (p, ('Default',)) if default else None,
            error = (p, ('Error',)) if error else None)

    @staticmethod
    def test1_switch_print(*s: [int], default: bool = True, error: bool = True):
        assert len(s) < 2

        p: Callable[[Tuple], Iterable[str]] = lambda *st: st

        def printer(*args: [str, int]) -> int:
            print(*args)
            return args[1]

        a: [] = \
            list(s) + [
                (0, printer, ['Zero', 0]),
                (1, printer, ['One', 1]),
                (2, printer, ['Two', 2]),
                (3, printer, ['Three', 3])
            ] if len(s) == 1 else []
        return switch(
            *a,
            default = (p, ('Default',)) if default else None,
            error = (p, ('Error',)) if error else None)

    @classmethod
    def test1_switch(cls):
        try:
            print('Testing flat')
            print('Test 1.1.1 returned ', cls.test1_switch_flat_print(), '.', sep = '')
            print('Test 1.1.2 returned ', cls.test1_switch_flat_print(1), '.', sep = '')
            print('Test 1.1.3 returned ', cls.test1_switch_flat_print(2), '.', sep = '')
            print('Test 1.1.4 returned ', cls.test1_switch_flat_print(3), '.', sep = '')
            print('Test 1.1.5 returned ', cls.test1_switch_flat_print(4), '.', sep = '')
            print('Test 1.1.e returned ', cls.test1_switch_flat_print(4), '.', sep = '')
            print('Test 1.1.d returned ', cls.test1_switch_flat_print(4, default = False), '.', sep = '')
            print('Test 1.1.b returned ', cls.test1_switch_flat_print(4, error = False), '.', sep = '')
            print('Test 1.1.r returned ', cls.test1_switch_flat_print(4, default = False, error = False), '.', sep = '')
        except Exception as e:
            print('Error 1', e)
        try:
            print('Testing grouped')
            print('Test 1.2.1 returned ', cls.test1_switch_print(), '.', sep = '')
            print('Test 1.2.2 returned ', cls.test1_switch_print(1), '.', sep = '')
            print('Test 1.2.3 returned ', cls.test1_switch_print(2), '.', sep = '')
            print('Test 1.2.4 returned ', cls.test1_switch_print(3), '.', sep = '')
            print('Test 1.2.5 returned ', cls.test1_switch_print(4), '.', sep = '')
            print('Test 1.2.e returned ', cls.test1_switch_print(4), '.', sep = '')
            print('Test 1.2.d returned ', cls.test1_switch_print(4, default = False), '.', sep = '')
            print('Test 1.2.b returned ', cls.test1_switch_print(4, error = False), '.', sep = '')
            print('Test 1.2.r returned ', cls.test1_switch_print(4, default = False, error = False), '.', sep = '')
        except Exception as e:
            print('Error 2', e)
        print('Done Test 1\n')

    @staticmethod
    def test2_switch_flat_print(*s, default: bool = True, error: bool = True):
        assert len(s) < 2

        p: Callable[[Tuple], Iterable[str]] = lambda *st: st

        a: [] = \
            list(s) + [
                0, ['Zero', 0],
                1, ['One', 1],
                2, ['Two', 2],
                3, ['Three', 3]
            ] if len(s) == 1 else []
        return switch_flat(
            *a,
            default = (p, ('Default',)) if default else None,
            error = (p, ('Error',)) if error else None)

    @staticmethod
    def test2_switch_print(*s, default: bool = True, error: bool = True):
        assert len(s) < 2

        p: Callable[[Tuple], Iterable[str]] = lambda *st: st

        a: [] = \
            list(s) + [
                (0, ['Zero', 0]),
                (1, ['One', 1]),
                (2, ['Two', 2]),
                (3, ['Three', 3])
            ] if len(s) == 1 else []
        return switch(*a, default = (p, ('Default',)) if default else None, error = (p, ('Error',)) if error else None)

    @classmethod
    def test2_switch(cls):
        try:
            print('Testing flat')
            print('Test 2.1.1 returned ', cls.test2_switch_flat_print(), '.', sep = '')
            print('Test 2.1.2 returned ', cls.test2_switch_flat_print(1), '.', sep = '')
            print('Test 2.1.3 returned ', cls.test2_switch_flat_print(2), '.', sep = '')
            print('Test 2.1.4 returned ', cls.test2_switch_flat_print(3), '.', sep = '')
            print('Test 2.1.5 returned ', cls.test2_switch_flat_print(4), '.', sep = '')
            print('Test 2.1.e returned ', cls.test2_switch_flat_print(4), '.', sep = '')
            print('Test 2.1.d returned ', cls.test2_switch_flat_print(4, default = False), '.', sep = '')
            print('Test 2.1.b returned ', cls.test2_switch_flat_print(4, error = False), '.', sep = '')
            print('Test 2.1.r returned ', cls.test2_switch_flat_print(4, default = False, error = False), '.', sep = '')
        except Exception as e:
            print('Error 1', e)
        try:
            print('Testing grouped')
            print('Test 2.2.1 returned ', cls.test2_switch_print(), '.', sep = '')
            print('Test 2.2.2 returned ', cls.test2_switch_print(1), '.', sep = '')
            print('Test 2.2.3 returned ', cls.test2_switch_print(2), '.', sep = '')
            print('Test 2.2.4 returned ', cls.test2_switch_print(3), '.', sep = '')
            print('Test 2.2.5 returned ', cls.test2_switch_print(4), '.', sep = '')
            print('Test 2.2.e returned ', cls.test2_switch_print(4), '.', sep = '')
            print('Test 2.2.d returned ', cls.test2_switch_print(4, default = False), '.', sep = '')
            print('Test 2.2.b returned ', cls.test2_switch_print(4, error = False), '.', sep = '')
            print('Test 2.2.r returned ', cls.test2_switch_print(4, default = False, error = False), '.', sep = '')
        except Exception as e:
            print('Error 2', e)
        print('Done Test 2\n')

    @classmethod
    def test_all_switches(cls):
        cls.test1_switch()
        cls.test2_switch()


if __name__ == '__main__':
    SwitchTests.test_all_switches()
