#!/usr/bin/python3
from threading import Lock as LockingPrimitive, local as env


class Locker:
    _lock1: LockingPrimitive

    def __init__(self, new_primitive: LockingPrimitive = None, auto_lock: bool = False):
        if new_primitive is None:
            self._lock1 = LockingPrimitive()
        else:
            self._lock1 = new_primitive
        if auto_lock:
            self.on()

    def __del__(self):
        self.off()

    def __enter__(self):
        self.on()

    def __exit__(self, *_):
        self.off()

    def on(self, blocking: bool = True, timeout: float = -1, trial: bool = True):
        try:
            return self.acquire(blocking, timeout)
        except Exception as e:
            if trial:
                return e
            else:
                raise

    def off(self, trial: bool = True):
        try:
            return self.release()
        except Exception as e:
            if trial:
                return e
            else:
                raise

    def acquire(self, blocking: bool = True, timeout: float = 0):
        return self._lock1.acquire(blocking, timeout)

    def release(self):
        return self._lock1.release()

    def locked(self) -> bool:
        return self._lock1.locked()


class Mutex(Locker):
    _lock2: Locker

    def __init__(self, lock: Locker, auto_lock: bool = False):
        Locker.__init__(self, lock._lock1, auto_lock = auto_lock)
        self._lock2 = lock
        if auto_lock:
            self.on()

    def __del__(self):
        self.off()

    def __enter__(self):
        self.on()

    def __exit__(self, *_):
        self.off()

    def on(self, blocking: bool = True, timeout: float = -1, trial: bool = True):
        return self._lock2.on(blocking, timeout, trial)

    def off(self, trial: bool = True):
        return self._lock2.off(trial)

    def acquire(self, blocking: bool = True, timeout: float = 0):
        return self._lock2.acquire(blocking, timeout)

    def release(self):
        return self._lock2.release()

    def locked(self) -> bool:
        return self._lock2.locked()


class Fregu:
    _id_current: int
    _lock: Locker

    def __init__(self):
        self._id_current = 0
        self._lock = Locker()

    def free_event_guard_unique(self) -> int:
        with Mutex(self._lock):
            self._id_current += 1
            e: env = env()
            e.x = self._id_current
            return e.x

    def run(self) -> int:  # alias
        return self.free_event_guard_unique()
