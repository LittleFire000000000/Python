#!/usr/bin/python3
from typing import List, Tuple, Dict, Callable, Any, Iterable, ItemsView, Union
from enum import IntEnum, unique

from parallel.multithreading import *
from parallel.ids import *

from threading import Event
from time import sleep

_calculation_phase_ids: IdSmugglerBase = IdSmugglerBase()


@unique
class CalculationPhases(IntEnum):
    """
    Facilitate the execution-sequence of commands necessary to complete parallel computation.
    Phases of Parallelism().
    """
    INITIALISE: int = _calculation_phase_ids.next_id()
    SET_OPERATING_PARAMETERS: int = _calculation_phase_ids.next_id()
    FINALIZE_OPERATING_PARAMETERS: int = _calculation_phase_ids.next_id()

    # MAIN CYCLE START
    SPAWN_THREADS: int = _calculation_phase_ids.next_id()
    TELL_THREADS_GO: int = _calculation_phase_ids.next_id()
    MONITOR_THREADS: int = _calculation_phase_ids.next_id()

    SEE_THREADS_STOP: int = _calculation_phase_ids.next_id()
    SEE_BATCH_END: int = _calculation_phase_ids.next_id()
    # MAIN CYCLE END

    FINALIZE: int = _calculation_phase_ids.next_id()

    @staticmethod
    def start() -> 'CalculationPhases':
        """
        Indicate the beginning of the execution-sequence.
        :return: CalculationPhases
        """
        return CalculationPhases(0)

    def has_ended(self) -> bool:
        """
        Indicate whether this phase concludes the execution-sequence.
        :return: bool
        """
        return self == self.FINALIZE

    def next_phase(self) -> 'CalculationPhases':
        """"""
        if self.has_ended():
            return self
        else:
            return CalculationPhases(self.value + 1)


class Runner:
    """
    Provide a standard for executing functions (and concluding the execution thereof).
    """
    _start_this_: Callable[[int, int], Any]  # batch number, slot number
    _ask_to_stop: Callable[[int, int], Any]  # batch number, slot number

    def __init__(self,
                 fxn: Callable[[int, int], Any] = None,
                 end: Callable[[int, int], Any] = None):
        """
        Load a function to be executed on parallel.
        :param fxn: Callable accepting two integers.
        :param end: Callable accepting two integers.
        When called, fxn receives the batch number (an int) and the slot number (int).
        """
        self._start_this_ = fxn
        self._ask_to_stop = end

    def run(self, batch: int, slot: int) -> Any:
        """
        Call the fxn loaded to start processing.
        This is typically only invoked by the parallelism machinery.
        :param batch: positive int
        :param slot: positive int
        :return:
        """
        if isinstance(self._start_this_, Callable):
            return self._start_this_(batch, slot)

    def end(self, batch: int, slot: int) -> Any:
        """
        Call the fxn loaded to signal a request to conclude processing.
        This is typically only invoked by the parallelism machinery.
        :param batch: positive int
        :param slot: positive int
        :return:
        """
        if isinstance(self._ask_to_stop, Callable):
            return self._ask_to_stop(batch, slot)

    @property
    def fxn(self) -> Callable[[int, int], Any]:
        return self._start_this_

    @property
    def fxn_end(self) -> Callable[[int, int], Any]:
        return self._ask_to_stop


class Cycle:
    """
    Cycle through an iterable.
    """
    __placeholder: int  # index
    __iterator_current: iter  # iterator from which to draw
    __iterator_raw: iter  # iterator from which to reset

    def _iterate(self, give_stop: bool):
        self.__placeholder += 1
        if self.__placeholder == 0:
            self.__iterator_current = iter(self.__iterator_raw)
        try:
            yield next(self.__iterator_current)
        except StopIteration:
            if give_stop:
                raise
            self.__placeholder = -1
            yield from self._iterate(False)

    def __init__(self, an_iterable: iter):
        """
        Declare a new cycle.
        :param an_iterable: an iterable object
        """
        self.give_iterable(an_iterable)

    # Setup

    def give_iterable(self, iterable: iter):
        """
        Set the cycle with which to operate.
        :param iterable: any iterable
        :return:
        """
        self.__placeholder = -1
        self.__iterator_raw = iterable
        return

    def retrieve_iterable(self) -> iter:
        """
        Retrieve the cycle with which this generator is operating.
        :return: an iterable
        """
        return self.__iterator_raw

    # Iterate

    def next(self, give_stop: bool = False) -> iter:
        """
        Generator the cycle.
        If give_stop is False, loop to the beginning of the cycle after conclusion,
        If give_stop is True, raise StopIteration at the end of the Cycle, instead of looping.
        :param give_stop: bool stop or loop
        :return: generator
        """
        while True:
            yield next(self._iterate(give_stop))

    def get_iteration(self) -> int:
        """
        What is the index of the item in the cycle currently observed.
        :return: int index
        """
        return self.__placeholder


class BatchExecutionOrder(Cycle):
    """
    Tell the sequence in which batches are executed--yield their order.
    Each iteration should yield a unique integer in range [0, ending_point) from all previous yields.
    No two yields should match and every integer in the range should been yielded once and, therefore only once.
    """
    _ending_point: int
    _quota_completed: int

    def __init__(self, an_iterable: iter, ending_point: int):
        """
        Initialize this sequencer to yield values in range [0, ending_point) in an order dictated by an_iterable.
        Each iteration should yield a unique value.  By the final iteration, it should've exhausted this range.
        The ending_point is a quota of iteration on this sequencer.
        :param an_iterable:
        :param ending_point:
        """
        Cycle.__init__(self, an_iterable)
        self._ending_point = ending_point
        self._quota_completed = 0

    def get_ending_point(self) -> int:
        """
        Return the ending_point of the range of this sequencer.
        That is, how many batches should be executed.
        :return: int
        """
        return self._ending_point

    def get_quota(self) -> int:
        """
        Return the number of iterations thus far completed towards this sequencer's quota.
        :return: int
        """
        return self._quota_completed

    def __iter__(self):
        yield from self.next(True)

    def give_iterable(self, iterable: iter):
        self._quota_completed = 0
        Cycle.give_iterable(self, iterable)

    def retrieve_iterable(self) -> iter:
        return Cycle.retrieve_iterable(self)

    def next(self, give_stop: bool = False) -> iter:
        while True:
            self._quota_completed += 1  # one done
            yield next(Cycle.next(self, give_stop))

    def is_quota_meet(self) -> bool:
        """
        Indicate whether a quota has been met.
        :return: bool fulfilled
        """
        return self._ending_point <= self._quota_completed

    def get_iteration(self) -> int:
        return Cycle.get_iteration(self)

    def full_next(self, give_stop: bool = True):
        """
        Give the next value in the sequence.
        >>> next(self.next(give_stop))
        :return:
        """
        return next(self.next(give_stop))


class Parallelism:
    """
    Enact the execution-sequence of commands necessary for complete parallel computation.
    """
    _phase: CalculationPhases

    def _check_phase(self, expected: CalculationPhases) -> bool:
        """
        Return whether this executor is in the given phase.
        :param expected: CalculationPhases
        :return: bool match
        """
        return expected == self._phase

    def _advance_phase(self):
        """
        Progress the current phase one forward.
        :return:
        """
        self._phase = self._phase.next_phase()

    def __init__(self, start_now: bool = True):
        """
        Create an instance of an executor.  Call start() if start_now.
        """
        self._phase = CalculationPhases.start()
        if start_now:
            self.start()

    # CalculationPhases.INITIALISE

    _batches: int  # how many grouped launches to execute in succession
    _slots: int  # how many threads to launch in parallel
    _results: Dict[int, Dict[int, Any]]  # results[batch][slot] = <result of call>

    def start(self) -> bool:
        """
        Prepare this executor for use after creation and initialization.
        Phase: CalculationPhases.INITIALISE
        :return: successfully started or not
        """
        if self._check_phase(CalculationPhases.INITIALISE):
            self._batches = 0
            self._slots = 0
            self._results = dict()
            self._advance_phase()
            return True
        return False

    # CalculationPhases.SET_OPERATING_PARAMETERS

    def set_number_of_batches(self, batches: int) -> bool:
        """
        Set the number of batches to be queued.
        This represents how many successive times the thread-pool is invoked.
        Phase: CalculationPhases.SET_OPERATING_PARAMETERS
        :param batches: whole number
        :return: successfully set or not
        """
        if self._check_phase(CalculationPhases.SET_OPERATING_PARAMETERS):
            self._batches = batches
            return True
        return False

    def get_batches(self) -> int:
        """
        Return the number of batches queued.
        Phase: Any
        :return: whole number
        """
        return self._batches

    def set_number_of_slots(self, slots: int) -> bool:
        """
        Set the number of slots to be queued.
        This represents how many successive threads/slots are in the thread-pool per batch.
        Phase: CalculationPhases.SET_OPERATING_PARAMETERS
        :param slots: whole number
        :return: successfully set or not
        """
        if self._check_phase(CalculationPhases.SET_OPERATING_PARAMETERS):
            self._slots = slots
            return True
        return False

    def get_slots(self) -> int:
        """
        Return the number of slots queued.
        Phase: Any
        :return: whole number
        """
        return self._slots

    def generate_batches_and_slots(self) -> bool:
        """
        Move from phase CalculationPhases.SET_OPERATING_PARAMETERS to CalculationPhases.FINALIZE_OPERATING_PARAMETERS.
        Phase: CalculationPhases.SET_OPERATING_PARAMETERS
        :return: successfully progressed or not
        """
        if self._check_phase(CalculationPhases.SET_OPERATING_PARAMETERS):
            if self._batches > 0 and self._slots > 0:
                self._advance_phase()
                return True
        return False

    # CalculationPhases.FINALIZE_OPERATING_PARAMETERS

    _signal_go: Event  # tell all threads go
    _signal_stop: Event  # ask all threads to stop

    _number_threads_started_lock: Locker
    _number_threads_stopped_lock: Locker
    _number_threads_stopped2_lock: Locker

    _read_write_lock: Locker
    _monitoring_lock: Locker

    _number_threads_started: int
    _number_threads_stopped: int
    _number_threads_stopped2: int

    _fxn: Runner
    _current_batch: int
    _monitoring: bool

    def set_executor(self, fxn: Runner) -> bool:
        """
        Provide a function to be executed on parallel.
        This is mandatory.
        Phase: CalculationPhases.FINALIZE_OPERATING_PARAMETERS
        :param fxn: a Runner instance
        :return: successfully set or not
        """
        if self._check_phase(CalculationPhases.FINALIZE_OPERATING_PARAMETERS):
            self._fxn = fxn
            return True
        return False

    def has_executor(self) -> bool:
        """
        Indicate whether a function has been provided.
        Phase: Any
        :return: bool present
        """
        if self._phase < CalculationPhases.FINALIZE_OPERATING_PARAMETERS:
            return False  # too early
        elif self._check_phase(CalculationPhases.FINALIZE_OPERATING_PARAMETERS):
            return self._fxn is not None
        return True

    _iter_order: BatchExecutionOrder

    def set_batch_execution_order(self, order: BatchExecutionOrder) -> bool:
        """
        Provide an order in which the batches are executed.
        If order is None, a default, boring, linear execution is applied.
        Phase: CalculationPhases.FINALIZE_OPERATING_PARAMETERS
        :param order: a BatchExecutionOrder instance or None
        :return: successfully assigned or not
        """
        if self._check_phase(CalculationPhases.FINALIZE_OPERATING_PARAMETERS):
            self._iter_order = order
            return True
        return False

    def has_batch_execution_order(self) -> bool:
        """
        Indicate whether an order has been provided.
        Phase: Any
        :return: bool present
        """
        if self._phase < CalculationPhases.FINALIZE_OPERATING_PARAMETERS:
            return False  # too early
        elif self._check_phase(CalculationPhases.FINALIZE_OPERATING_PARAMETERS):
            return self._iter_order is not None
        return True

    def prepare_to_spawn_thread(self) -> bool:
        """
        Before batches can be executed, this function prepares the apparatus.
        Phase: CalculationPhases.FINALIZE_OPERATING_PARAMETERS
        :return: successfully done or not
        """
        if self._check_phase(CalculationPhases.FINALIZE_OPERATING_PARAMETERS):
            if self._fxn is not None:  # If no fxn is given, this is pointless.
                if self._iter_order is None:
                    self._iter_order = BatchExecutionOrder(range(self._batches), self._batches)
                #
                self._signal_go = Event()
                self._signal_stop = Event()
                self._number_threads_started_lock = Locker()
                self._number_threads_stopped_lock = Locker()
                self._number_threads_stopped2_lock = Locker()
                self._read_write_lock = Locker()
                self._monitoring_lock = Locker()
                self._number_threads_started = 0
                self._number_threads_stopped = 0
                self._number_threads_stopped2 = 0
                self._current_batch = 0
                #
                self._advance_phase()
                return True
        return False

    # CalculationPhases.SPAWN_THREADS

    def __run(self, batch: int, slot: int):
        """ Execute the given function. """

        # READY: prepare for start
        with Mutex(self._number_threads_started_lock):
            self._number_threads_started += 1
        # SET: wait for start signal
        self._signal_go.wait()
        # GO!: invoke function on parallel
        tmp: env = env()
        tmp.x = self._fxn.run(batch, slot)
        if tmp.x is not None:
            with Mutex(self._read_write_lock):
                self._current_batch_results_ref[slot] = tmp.x  # conserve memory
        del tmp
        # SLOW: acknowledge stop
        with Mutex(self._number_threads_stopped_lock):
            self._number_threads_stopped += 1
        # STOP: wait for stop signal
        self._signal_stop.wait()
        self._fxn.end(batch, slot)
        # STOP...
        with Mutex(self._number_threads_stopped2_lock):
            self._number_threads_stopped2 += 1
        return

    _current_batch_results_ref: Dict[int, Any]

    def spawn_threads(self) -> int:
        """
        Spawn the thread-pool for this batch.
        This function returns an integral indicator where:
            0 means inappropriate time to call
            1 means all slots/threads for this batch successfully spawned
            2 means all batches have been already executed
        Phase: CalculationPhases.SPAWN_THREADS
        :return: int indicator
        """
        if self._check_phase(CalculationPhases.SPAWN_THREADS):
            if self._iter_order.is_quota_meet():
                self._phase = CalculationPhases.FINALIZE
                return 2  # done already
            else:
                self._current_batch = self._iter_order.full_next()
                t = {}
                self._results[self._current_batch] = t
                self._current_batch_results_ref = t
                for slot in range(self._slots):
                    Thread(target = self.__run, args = (self._current_batch, slot)).start()
                return 1  # all launched
        return 0  # bad call

    def prepare_to_invoke_calls(self) -> int:
        """
        Transition from phase CalculationPhases.SPAWN_THREADS to CalculationPhases.TELL_THREADS_GO.
        This function returns an integral indicator where:
            0 means inappropriate time to call
            1 means though threads may have been launched, not all have finished spawning
            2 means all threads are done spawn and the transfer has completed
        Phase: CalculationPhases.SPAWN_THREADS
        :return: int indicator
        """
        if self._check_phase(CalculationPhases.SPAWN_THREADS):
            with Mutex(self._number_threads_started_lock):
                if self._number_threads_started == self._slots:  # all threads now await the GO! signal
                    self._advance_phase()
                    return 2  # spawning complete
                else:
                    return 1  # still spawning
        return 0  # bad call

    # CalculationPhases.TELL_THREADS_GO

    def begin_all_invocations(self) -> bool:
        """
        Instruct all the threads to begin executing the function.
        Phase: CalculationPhases.TELL_THREADS_GO
        :return: successfully done or not
        """
        if self._check_phase(CalculationPhases.TELL_THREADS_GO):
            self._signal_go.set()
            self._monitoring = False
            self._advance_phase()
            return True
        return False

    # CalculationPhases.MONITOR_THREADS

    def turn_monitoring_on(self, on_not_off: bool = True):
        """
        Activate or deactivate a thread-progress monitoring session.
        If one has already been activated, False will be returned.
        Phase: CalculationPhases.MONITOR_THREADS
        :param on_not_off: activate
        :return: successfully done or not
        """
        if self._check_phase(CalculationPhases.MONITOR_THREADS):
            if on_not_off:
                if self._monitoring:
                    return False
                self._read_write_lock.acquire()
                self._monitoring = True
            elif not self._monitoring:
                self._monitoring = False
                self._read_write_lock.release()
            return True
        return False

    def is_monitoring_turned_on(self) -> bool:
        """
        Tell whether a thread-progress monitoring session has been activated.
        Phase: CalculationPhases.MONITOR_THREADS
        :return: successfully done or not
        """
        if self._check_phase(CalculationPhases.MONITOR_THREADS):
            with Mutex(self._read_write_lock):
                return self._monitoring
        return False

    def get(self, slot: int):  # todo doc
        """"""
        return self._current_batch_results_ref.get(slot, 0)

    def index_slot_from_value(self, candidate) -> int:
        """"""
        for i, v in self._current_batch_results_ref.items():
            if v == candidate:
                return i
        return -1

    def find_things(self, things: set) -> [int, Any]:
        """"""
        for i, v in self._current_batch_results_ref.items():
            if v in things:
                yield i, v
        yield -1, 0

    def filter(self, candidate: Any, filtered: Callable[[ItemsView[int, Any], Any], Any]) -> Any:
        """"""
        return filtered(self._current_batch_results_ref.items(), candidate)

    def conclude_threads(self) -> int:
        """"""
        if self._check_phase(CalculationPhases.MONITOR_THREADS):
            with Mutex(self._number_threads_stopped_lock):
                if self._number_threads_stopped == self._slots:
                    self._signal_stop.set()
                    self._advance_phase()
                    return 2
                else:
                    return 1
        else:
            return 0

    # CalculationPhases.SEE_THREADS_STOP

    def finalize_batch(self, continue_batches: bool = True) -> bool:
        """"""
        if self._check_phase(CalculationPhases.SEE_THREADS_STOP):
            with Mutex(self._number_threads_stopped2_lock):
                if self._number_threads_stopped2 == self._slots:
                    if len(self._current_batch_results_ref) == 0:
                        del self._results[self._current_batch]
                    self._phase = CalculationPhases.SPAWN_THREADS if continue_batches else CalculationPhases.SEE_BATCH_END
                    return True
        return False

    def count_batch_results(self) -> Union[int, None]:
        """"""
        if self._check_phase(CalculationPhases.SEE_THREADS_STOP):
            return len(self._current_batch_results_ref)
        return None

    # CalculationPhases.SEE_BATCH_END

    # CalculationPhases.FINALIZE


_calculation_phase_ids.advance_id(-_calculation_phase_ids.next_id())


@unique
class RunParallelPhases(IntEnum):
    """
    .
    """

    BATCH_SLOT_ERROR: int = _calculation_phase_ids.next_id()
    MONITORING: int = _calculation_phase_ids.next_id()
    MONITORING_ACQUISITION_ISSUE: int = _calculation_phase_ids.next_id()
    MONITORING_RELEASE_ISSUE: int = _calculation_phase_ids.next_id()
    BATCH_RESULT: int = _calculation_phase_ids.next_id()
    CONCLUSION: int = _calculation_phase_ids.next_id()


RPP = RunParallelPhases


def run_parallel(
        fxn: Callable[[int, int], Any], fxn_end: Callable[[int, int], Any],
        batches: int = 1, slots: int = 1,
        batch_order: BatchExecutionOrder = None,
        yield_to_monitor: bool = True,
        auto_lock_unlock_monitoring: bool = True,
        monitoring_wait: float = .02,
        spawn_wait: float = .02,
        conclusion_wait: float = .02
) -> [Tuple[Parallelism, RPP, int]]:
    """"""
    obj: Parallelism = Parallelism(True)
    # Initialization
    obj.set_number_of_batches(batches)
    obj.set_number_of_slots(slots)
    if not obj.generate_batches_and_slots():
        yield obj, RPP.BATCH_SLOT_ERROR, 0
    obj.set_executor(Runner(fxn, fxn_end))
    obj.set_batch_execution_order(batch_order)
    # Main Cycle:  Batch by Batch with Parallel Slots
    obj.prepare_to_spawn_thread()
    total: int = 0
    a: int = 0
    while obj.spawn_threads() == 1:
        while obj.prepare_to_invoke_calls() == 1:
            sleep(spawn_wait)
        obj.begin_all_invocations()
        if yield_to_monitor:
            if auto_lock_unlock_monitoring:
                sleep(monitoring_wait)
                if obj.turn_monitoring_on(True):
                    yield obj, RPP.MONITORING, a
                else:
                    yield obj, RPP.MONITORING_ACQUISITION_ISSUE, a
                if not obj.turn_monitoring_on(False):
                    yield obj, RPP.MONITORING_RELEASE_ISSUE, a
            else:
                yield obj, RPP.MONITORING, a
        while obj.conclude_threads() == 1:
            sleep(conclusion_wait)
        a = obj.count_batch_results()
        if a > 0:
            yield obj, RPP.BATCH_RESULT, a
            total += a
        obj.finalize_batch(True)
    return obj, RPP.CONCLUSION, total
