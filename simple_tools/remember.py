#!/usr/bin/python3
from os.path import isfile
from ast import parse as ast_parser
from typing import Tuple, Union, Callable, Any

import simple_tools.a_collect as a_collect


class Error(Exception):
    """This is the generic error skeleton."""

    def __init__(self, msg = ""): self.msg = msg

    def __str__(self): return self.msg


class LoadingError(Error):
    """Something isn't loaded."""
    pass


class TargetError(Error):
    """An invalid document filename or option was entered."""
    pass


class WrappingError(Error):
    """Some options conflict with each other."""
    pass


# noinspection PyUnresolvedReferences,PyUnresolvedReferences,PyUnresolvedReferences,PyIncorrectDocstring
class Memory(object):
    """This class is a Data Storage and Retrieval API."""

    __loaded = False
    __str_wrapping = False
    __force_type = True
    __encoding = None
    __data_type = dict
    __memories = dict()
    __target = None

    def __init__(self, mem, target, data_type = dict, force_type = True, string_wrap = False,
                 target_encoding = 'UTF-8'):
        """Specify a piece of data (No classes or functions that can not be properly represented) that can be
            initialized for "mem".
        Give a file name or None for "target" (Document) to target a file (If None is specified, be sure to invoke the
            target method later).
        Make sure "data_type" is the data type of "mem".
        The "force_type" option must be a boolean value:
            What it does is enforce the data_type on the data.
            When the recall method is invoked, if the file already exists, this API will convert it's content into the
                data_type.
        The "string_wrap" feature allows the API to read documents of text as strings.
        "string_wrap" Must be a boolean value:
            If True, the data_type of this API must be a string.
        The "target_encoding" is the encoding of the file being targeted."""

        assert isinstance(mem, data_type), "Takes only a {}.".format(type(data_type))
        if not (target is None or isinstance(target, str)):
            raise TargetError("\"Target\" Must be either a string or None.")
        assert isinstance(string_wrap, bool), "\"string_wrap\" Must be a boolean value."
        self.__loaded = target not in (None, "")
        self.__memories = data_type()
        self.__data_type = data_type
        self.__force_type = force_type
        self.__encoding = target_encoding
        self.set_string_wrapping_state(string_wrap)
        self.target(target)
        self.set_memories(mem)

    def __del__(self):
        """The destructor of this API calls the "remember" method when ever this APIs object is lost."""

        if self.is_active():
            self.remember()

    def __eq__(self, o):
        """Returns True if "o" is Equal to the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__eq__(o)
        except Exception:
            return False

    def __ne__(self, o):
        """Returns True if "o" is Not equal to the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__ne__(o)
        except Exception:
            return False

    def __lt__(self, o):
        """Returns True if "o" is Less than the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__lt__(o)
        except Exception:
            return False

    def __gt__(self, o):
        """Returns True if "o" is Greater than the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__gt__(o)
        except Exception:
            return False

    def __le__(self, o):
        """Returns True if "o" is Less than or equal to the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__le__(o)
        except Exception:
            return False

    def __ge__(self, o):
        """Returns True if "o" is Greater than or equal to the piece of data being held by this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            return self.get_memories().__ge__(o)
        except Exception:
            return False

    def __pos__(self):
        """Provides functionality for +<num>."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__pos__()

    def __neg__(self):
        """Provides functionality for -<num>."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__neg__()

    def __abs__(self):
        """Provides functionality for abs-ing."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__abs__()

    def __invert__(self):
        """Provides functionality for ~."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__invert__()

    def __round__(self, num):
        """Provides functionality for rounding."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__round__(num)

    def __floor__(self):
        """Provides functionality for math.floor-ing."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__floor__()

    def __ceil__(self):
        """Provides functionality for math.ceil-ing."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__ceil__()

    def __trunc__(self):
        """Provides functionality for math.trunc-ing."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__trunc__()

    def __add__(self, obj):
        """Handles operator-overloading for +."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__add__(obj)

    def __sub__(self, obj):
        """Handles operator-overloading for ."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__sub__(obj)

    def __mul__(self, obj):
        """Handles operator-overloading for *."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__mul__(obj)

    def __div__(self, obj):
        """Handles operator-overloading for /."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__div__(obj)

    def __floordiv__(self, obj):
        """Handles operator-overloading for //."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__floordiv__(obj)

    def __truediv__(self, obj):
        """Handles operator-overloading for _true_ division."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__truediv__(obj)

    def __mod__(self, obj):
        """Handles operator-overloading for %."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__mod__(obj)

    def __divmod__(self, obj):
        """Handles operator-overloading for divmod()."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__divmod__(obj)

    def __pow__(self, obj):
        """Handles operator-overloading for **."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__pow__(obj)

    def __lshift__(self, obj):
        """Handles operator-overloading for <<."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__lshift__(obj)

    def __rshift__(self, obj):
        """Handles operator-overloading for >>."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__rshift__(obj)

    def __and__(self, obj):
        """Handles operator-overloading for &."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__and__(obj)

    def __or__(self, obj):
        """Handles operator-overloading for |."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__or__(obj)

    def __xor__(self, obj):
        """Handles operator-overloading for ^."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return self.get_memories().__xor__(obj)

    def __iter__(self):
        """When the class API is iterated over, it yields back through the current piece of data being held in this
        API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        # noinspection PyBroadException
        try:
            yield from self.get_memories().__iter__()
        except Exception:
            yield from (self.get_memories(),)

    def __bool__(self):
        """Replies as to whether or not this API in active."""

        assert not isinstance(self.get_memories(), bool), "Use \"get_memories\" or \"is_active\" instead."
        return self.is_active()

    def __repr__(self):
        """This returns the repr string of the current piece of data being held in this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return repr(self.get_memories())

    def __str__(self):
        """This returns a string value of the current piece of data being held in this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return str(self.get_memories())

    def __dict__(self):
        """This returns a string value of the current piece of data being held in this API."""

        if not self.is_active():
            raise LoadingError("Please initialize this API.")
        return dict(self.get_memories())

    def get_memories(self):
        """This method returns the current piece of data that is currently being held in this API."""

        return self.__memories

    def get_type(self):
        """This method retrieves the current data_type of the current piece of data that this currently being held in 
        this API."""

        return self.__data_type

    def get_type_enforcement_state(self):
        """This method returns the state of data_type enforcement that is currently being upheld by this API."""

        return self.__force_type

    def get_string_wrapping_state(self):
        """When called, this method returns the state of "document mode".
        This feature allows the API to read documents of text as strings."""

        return self.__str_wrapping

    def is_active(self):
        """This method will return weather or not the API is connected to a document."""

        self.__loaded = self.get_target() not in (None, "")
        return self.__loaded

    def get_target(self):
        """This method returns the current document's file name that is being targeted by this API."""

        return self.__target if self.__target is not None else ""

    def de_target(self, save):
        """All this method does is de-target the current document that is being targeted by this API.
        The "save" parameter must be a boolean value:
            If True, then this method will invoke the "remember" method.
            Regardless, the current piece of data being held by this API will remain intact.
        The "set_memories" and "get_memories" methods will remain operational.
        Be sure to have all the API settings favourable to the target being saved or the data might be lost."""

        assert isinstance(save, bool), "Only takes a boolean value."
        ty = 0
        if save:
            ty = self.remember()
        self.__target = None
        self.__loaded = False
        return ty

    def target(self, target, save = True):
        """This method is responsible for switching document targets.
        The "target" parameter must be a string:
            It tells this API which document to load.
            The current document is saved.
            By passing None as "target", unless no file is/was None, this API will see that as a signal to deactivate.
        The "save" parameter also must be a boolean value. If it is False, the current piece of data will not be saved.
        Be sure to have all the API settings favourable to the target being loaded or the data might be lost."""

        if not self.is_active():
            assert isinstance(target, str) or target is None, "\"target\" Must be a string."
        else:
            if target is None:
                if save:
                    return self.de_target(True)
                else:
                    raise WrappingError("Data lose while de-targeting.")
            else:
                assert isinstance(target, str) or target is None, "\"target\" Must be a string."
        ty = 0
        if save:
            if self.get_target() not in (None, ""):
                ty = 1 + self.remember()
        self.__target = target
        self.__loaded = target not in (None, "")
        self.recall()
        return ty

    def set_string_wrapping_state(self, string_wrap):
        """The "string_wrap" feature allows the API to read documents of text as strings.
        "string_wrap" Must be a boolean value:
            If True, the data_type of this API must be a string.
        "safe" Must also be a boolean value:
            If left False, the this API must be initialized."""

        assert isinstance(string_wrap, bool), "\"string_wrap\" Must be a boolean value."
        if string_wrap and not self.get_type() is str:
            raise WrappingError("The data_type of this API must be set to a string.")
        self.__str_wrapping = string_wrap
        return None

    def set_memories(self, memories):
        """This method sets the current piece of data that this currently being held in this API."""

        if self.get_type_enforcement_state():
            self.__memories = self.get_type()(memories)
        else:
            self.__memories = memories
        return None

    def set_type_enforcement_state(self, true):
        """This method sets the state of data_type enforcement that is currently being upheld by this API.
        This method only accepts a boolean value."""

        assert isinstance(true, bool), "This method only accepts a boolean value."
        self.__force_type = true
        if true:
            return self.set_type(self.get_type())
        return 0

    def set_type(self, type_, convert_ = True, save = True):
        """This method sets the data_type of the data that is currently being held in this API.
        By leaving "convert_" on, this API will convert the current piece of data that this currently being held into 
            the new data_type.
        Otherwise, the API will replace the currently stored data with a new instance of the new data_type:
            When "safe" is on -- in addition to converting the data -- it will also save the current data.
            To revert back to the current data, change the data_type back and invoke the recall method the best way you 
                see fit.
        In order to convert data_types, temporarily disable type_enforcement.
        Be warned that if the data_types aren't cross-translatable, the current data will be erased.
        The "string_wrap" feature allows the API to read documents of text as strings.
        If "document mode" is turned on, the data_type of this API must be a string."""

        if self.get_string_wrapping_state() and not self.get_type() is str:
            raise WrappingError("The data_type of this API must be set to a string.")
        self.__data_type = type_
        if self.get_type_enforcement_state():
            if convert_:
                # noinspection PyBroadException
                try:
                    self.set_memories(type_(self.get_memories()))
                    return 1
                except Exception:
                    self.set_memories(type_())
                    return 2
            else:
                ty = 3
                if save:
                    ty += 1 + self.remember()
                self.set_memories(type_())
                return ty
        return 0

    def check_type(self):
        """Calling this method confirms that the data is in the format of the current data_type.
        If type_enforcement is turn off, None is returned.
        The data_type of this API must be set to a string if string_wrapping is turned on."""

        if self.get_string_wrapping_state() and not self.get_type() is str:
            raise WrappingError("The data_type of this API must be set to a string.")
        if not self.get_type_enforcement_state():
            return None
        # noinspection PyTypeChecker
        return isinstance(self.get_memories(), self.get_type())

    def remember(self):
        """This method saves the current piece of data that this currently being held in this API to the document that 
        this currently being targeted by this API."""

        ty = 0
        if self.get_target() not in (None, ""):
            with open(self.get_target(), ("w+" if isfile(self.get_target()) else "x+"), encoding = self.__encoding) as \
                    mem:
                if not self.get_string_wrapping_state():
                    ty = 1
                    mem.write(str(repr(self.get_memories())))
                else:
                    ty = 2
                    # noinspection PyTypeChecker
                    mem.write(self.get_memories())
        return ty

    def recall(self):
        """This method recalls the data from the document that is currently being targeted by this API and sets it as 
           the current data.
        If the document currently being targeted doesn't exist, then this API will generate it and put the current data 
            into it.
        When this method is invoked, if the file already exists, this API will convert it's content into the predefined 
            data_type.
        Be sure to have all the API settings favourable to the target being loaded or the data might be lost."""

        ty = 0
        if self.get_target() not in (None, ""):
            if not isfile(self.get_target()):
                ty = 9 + self.remember()
            else:
                ty = 2
                mem = open(self.get_target(), 'r+', encoding = self.__encoding)
                a = mem.read()
                # noinspection PyBroadException
                try:
                    if not self.get_string_wrapping_state():
                        ty = 3

                        def safe():
                            nonlocal ty
                            if a != "" and ast_parser(a):  # Replace expression with AFF.
                                b = a
                                ty = 4
                            else:
                                b = repr(self.get_type()())
                            return b

                        s = safe()

                        self.set_memories(eval(
                            s,
                            {x: None for x in globals().keys()},
                            {x: None for x in locals().keys()}))
                    else:
                        ty = 5
                        self.set_memories(a)
                except Exception:
                    self.remember()
                # noinspection PyTypeChecker
                if not isinstance(self.get_memories(), self.get_type()):
                    ty = 6
                    if self.get_type_enforcement_state():
                        mem.close()
                        # noinspection PyBroadException
                        try:
                            self.set_memories(self.get_type()(self.get_memories()))
                            ty = 7
                        except Exception:
                            self.set_memories(self.get_type()())
                            ty = 8
                    self.remember()
                if ty not in (7, 8):
                    mem.close()
                del mem, a
        return ty


def modify_recalled_parameter(initial: int, prompt: str, minimum: int = None, maximum: int = None,
                              default_yes: bool = True) -> Tuple[int, Union[bool, None]]:
    """
    Modify a recalled value.  This is intended for use in conjunction with remember.Memory().
    If initial is None, a new value is prompted and returned.
    >>> return new()
    The numeric bounds of a value are checked by evaluating:
    >>> a_collect.is_within_bounds(initial, minimum, maximum)
    If the bounds are met, it is prompted whether initial should be kept/renewed.
    If it's kept, it's returned; otherwise, a new value is prompted and returned.
    And finally, if the bounds weren't met, a new value is prompted and returned.
    When prompting, if default_yes, just hitting [Enter] registers as a yes, else a no.
    
    The user indicator is:
        True if the users signaled Yes,
        False if the user signaled No,
        None if the user didn't signal either
    -
    
    :param initial: initial state of information
    :param prompt: query for information
    :param minimum: lower bound
    :param maximum: upper bound
    :param default_yes: bool
    :return: tuple (modified state of information, user indicator)
    """

    def new():
        nonlocal prompt, minimum, maximum
        return a_collect.get_input_advanced(prompt, minimum = minimum, maximum = maximum)

    if initial is None:  # the initial value is unknown
        return new(), None
    elif a_collect.is_within_bounds(initial, minimum, maximum):
        prompt_yn: str = f'Should "{prompt}" stay {initial} [Y] or change [N]: '

        while True:
            answer = input(prompt_yn).lower().strip()
            if len(answer):
                answer = answer[0]
                if answer in 'yes1':
                    answer = True
                    break
                elif answer in 'no0':
                    answer = False
                    break
                else:
                    print('Unrecognized input.')
            else:
                answer = default_yes
                break

        if answer:
            return initial, True
        else:
            return new(), False
    else:
        return new(), None


fields_to_recall: Callable[[object], int] = \
    lambda obj: len(list(x for x in dir(obj) if not (x.startswith('_') or x.startswith('v_'))))
fields_to_recall.__doc__ = """Give the number of (public) variables in a class or an object."""

fields_to_fill: Callable[[list, int, Any], None] = lambda given_list, expected_length, fill_value = None: \
    given_list.extend(
        [] if len(given_list) >= expected_length else ([fill_value] * (expected_length - len(given_list))))
fields_to_fill.__doc__ = \
    """Make sure a given_list is of at least the expected_length using fill_value to fill the missing length."""
