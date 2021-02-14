#!/usr/bin/python3
from threading import Lock, Thread
from time import sleep

LOADING: str = '[|/-\\|]_{^*v*<*>*}'
LOADING_LENGTH_MINUS_ONE: int = len(LOADING) - 1


class Reporter:
    _step: int
    _previous_length: int
    _pause: float
    _terminate: bool
    _value_lock: Lock
    _internal: Thread

    def __init__(self, pause: float):
        self._step = 0
        self._previous_length = 0
        self._pause = pause
        self._terminate = False
        self._value_lock = Lock()
        self._internal = Thread(target = self._runner, name = "Progress", daemon = True)
        self._internal.start()

    def stop(self):
        with self._value_lock:
            if self._terminate:
                return
            self._terminate = True
        self._internal.join()
        print('\r' + ' ' * self._previous_length + '\r', end = '', flush = True)

    def _runner(self):
        index = 0
        vl = self._value_lock
        while True:
            with vl:
                if self._terminate:
                    break
                output_string: str = f'{LOADING[index]} <{self._step}>.'
                print('\r' + output_string.ljust(self._previous_length), end = '', flush = True)
                index = (index + 1) if index < LOADING_LENGTH_MINUS_ONE else 0
                self._previous_length = len(output_string)
                pause = self._pause
            sleep(pause)
        return

    def is_running(self) -> bool:
        with self._value_lock:
            return not self._terminate

    def get_step(self) -> int:
        with self._value_lock:
            return self._step

    def set_step(self, step: int = 0):
        with self._value_lock:
            self._step = step

    def add_step(self, steps: int = 1):
        with self._value_lock:
            self._step += steps
