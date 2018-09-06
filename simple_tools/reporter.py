#!/usr/bin/python3
from threading import Thread, Lock, local
from time import sleep

LOADING: (str,) = ('|', '/', '-', '\\')
LOADING_LEN: int = len(LOADING)


class Store(local):
    index: int
    run: bool
    step: int
    total: int
    length: int


class Reporter:
    _value: int
    _total: int
    _previous_length: int
    _run: bool
    _value_lock: Lock
    _internal: Thread

    def __init__(self, total: int):
        self._value = 0
        self._total = total
        self._previous_length = 0
        self._run = False
        self._value_lock = Lock()
        #
        self._internal = Thread(target = self._runner, name = "Progress", daemon = True)
        self._internal.start()

    def __del__(self):
        self.stop()

    def stop(self):
        self._value_lock.acquire()
        if self._run:
            self._value_lock.release()
            return
        self._run = True
        self._value_lock.release()
        #
        self._internal.join()
        #
        self._value_lock.acquire()
        print('\r' + ' ' * self._previous_length + '\r', end = '', flush = True)
        self._value_lock.release()

    def _runner(self):
        store = Store()
        store.index = 0
        while True:
            self._value_lock.acquire()
            store.run = self._run
            store.step = self._value
            store.total = self._total
            store.length = self._previous_length
            self._value_lock.release()
            if store.run:
                break
            #
            output_string: str = 'Progress: {} of {}, {}%' \
                .format(store.step, store.total, store.step * 100 // store.total) \
                .ljust(store.length)
            store.length = len(output_string)
            print(f'\r{LOADING[store.index]} ' + output_string, end = '', flush = True)
            store.index += 1
            if store.index == LOADING_LEN:
                store.index = 0
            sleep(.5)
            #
            self._value_lock.acquire()
            self._previous_length = store.length
            self._value_lock.release()
        return

    def is_running(self) -> bool:
        tmp = local()
        self._value_lock.acquire()
        tmp.run = self._run
        self._value_lock.release()
        return not tmp.run

    def get_total(self) -> int:
        tmp = local()
        self._value_lock.acquire()
        tmp.total = self._total
        self._value_lock.release()
        return tmp.total

    def get_step(self) -> int:
        tmp = local()
        self._value_lock.acquire()
        tmp.step = self._value
        self._value_lock.release()
        return tmp.step

    def set_step(self, step: int = 0):
        Thread(target = self._set_step, name = "Setter", args = (self, step), daemon = True).start()

    @staticmethod
    def _set_step(self, step: int):
        self._value_lock.acquire()
        self._value = step
        self._value_lock.release()

    def add_step(self, steps: int = 1):
        Thread(target = self._add_step, name = "Adder", args = (self, steps), daemon = True).start()

    @staticmethod
    def _add_step(self, steps: int):
        self._value_lock.acquire()
        self._value += steps
        self._value_lock.release()
