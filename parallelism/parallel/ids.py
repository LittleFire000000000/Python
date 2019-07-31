#!/usr/bin/python3
from threading import *


class IdSmugglerBase:
    """
    Base class of IdSmuggler().
    Made for easy ID generation.
    """
    __id: int

    def __init__(self, starting_point: int = 0):
        """
        Setup this ID slot with the first ID being starting_point.
        :param starting_point: whole number
        """
        self.__id = starting_point

    def get_id(self) -> int:
        """
        Get the next ID pending assignment/ready to use.
        :return: int ID
        """
        return self.__id

    def next_id(self) -> int:
        """
        Get-to-use the next ID pending assignment/ready to use.
        :return: int ID
        """
        tmp: int = self.__id
        self.advance_id()
        return tmp

    def advance_id(self, number_of_times: int = 1):
        """
        Prepare the number_of_times-ahead ID for assignment.
        :param number_of_times: natural number
        :return:
        """
        self.__id += number_of_times
        return


class IDs(IdSmugglerBase):
    _lock: Lock

    def __init__(self, starting_point: int = 0):
        IdSmugglerBase.__init__(self, starting_point)
        self._lock = Lock()

    def get_id(self) -> int:
        self._lock.acquire()
        env = local()
        env.x = IdSmugglerBase.get_id(self)
        self._lock.release()
        return env.x

    def next_id(self) -> int:
        self._lock.acquire()
        env = local()
        env.x = IdSmugglerBase.next_id(self)
        self._lock.release()
        return env.x

    def advance_id(self, number_of_times: int = 1):
        self._lock.acquire()
        IdSmugglerBase.advance_id(self, number_of_times)
        self._lock.release()
