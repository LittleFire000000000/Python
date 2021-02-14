#!/usr/bin/python3
from collections import namedtuple
from ctypes import c_bool, c_uint
from io import BytesIO
from itertools import cycle
from multiprocessing import Event, Lock, Pipe, Process, Value
from typing import Callable, Generator, Tuple, Union


def p_value(v_type, *i_value, lock: Union[Lock, bool] = False) -> Value:
    return Value(v_type, *i_value, lock = lock)


def event_clear_wait(_ev: Event):
    _ev.clear()
    _ev.wait()


def event_wait_clear(_ev: Event):
    _ev.wait()
    _ev.clear()


class ProcessPairController:
    _event_1: Event
    _event_2: Event

    def __init__(self):
        self._event_1 = Event()
        self._event_2 = Event()

    @property
    def x1(self) -> bool:
        return self._event_1.is_set()

    @property
    def x2(self) -> bool:
        return self._event_2.is_set()

    def a_clear0wait1(self):
        self._event_2.clear()
        event_clear_wait(self._event_1)

    def a_clear0wait2(self):
        self._event_1.clear()
        event_clear_wait(self._event_2)

    def a_clear1wait1(self):
        event_clear_wait(self._event_1)

    def a_clear2wait2(self):
        event_clear_wait(self._event_2)

    def a_clear1wait2(self):
        self._event_1.clear()
        self._event_2.wait()

    def a_clear2wait1(self):
        self._event_2.clear()
        self._event_1.wait()

    def a_clear1set2(self):
        self._event_1.clear()
        self._event_2.set()

    def a_clear2set1(self):
        self._event_2.clear()
        self._event_1.set()

    def b_clear1set2wait1(self):
        (e1 := self._event_1).clear()
        self._event_2.set()
        e1.wait()

    def b_clear2set1wait2(self):
        (e2 := self._event_2).clear()
        self._event_1.set()
        e2.wait()

    def b_set1wait2clear2(self):
        self._event_1.set()
        event_wait_clear(self._event_2)

    def b_set2wait1clear1(self):
        self._event_2.set()
        event_wait_clear(self._event_1)

    def b_set1wait2clear1(self):
        (e1 := self._event_1).set()
        self._event_2.wait()
        e1.clear()

    def b_set2wait1clear2(self):
        (e2 := self._event_2).set()
        self._event_1.wait()
        e2.clear()

    def b_wait1clear1set2(self):
        event_wait_clear(self._event_1)
        self._event_2.set()

    def b_wait2clear2set1(self):
        event_wait_clear(self._event_2)
        self._event_1.set()

    def b_set1wait2(self):
        self._event_1.set()
        self._event_2.wait()

    def b_set2wait1(self):
        self._event_2.set()
        self._event_1.wait()

    def b_wait1set2(self):
        self._event_1.wait()
        self._event_2.set()

    def b_wait2set1(self):
        self._event_2.wait()
        self._event_1.set()

    def b_wait1clear1(self):
        event_wait_clear(self._event_1)

    def b_wait2clear2(self):
        event_wait_clear(self._event_2)

    def clear0(self):
        self._event_1.clear()
        self._event_2.clear()

    def clear1only(self):
        self._event_1.clear()

    def clear2only(self):
        self._event_2.clear()

    def set0(self):
        self._event_1.set()
        self._event_2.set()

    def set1only(self):
        self._event_1.set()

    def set2only(self):
        self._event_2.set()

    def wait0(self):
        self._event_1.wait()
        self._event_2.wait()

    def wait1only(self):
        self._event_1.wait()

    def wait2only(self):
        self._event_2.wait()


G_NONE = Generator[None, None, None]
GPE_TYPE = Callable[[], None]


def gpe_give_next(g: Callable[[ProcessPairController, ProcessPairController], Union[G_NONE, GPE_TYPE]]) -> Callable[[ProcessPairController, ProcessPairController], GPE_TYPE]:
    def inner(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:
        xg = g(a, b)
        return lambda: next(xg)

    return inner


class GeneratePPCExchange:
    @staticmethod
    @gpe_give_next
    def send_oscillate(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:  # FIRES FIRST!
        for x in cycle((a, b)):
            x.b_wait1clear1set2()
            yield

    @staticmethod
    @gpe_give_next
    def receive_oscillate(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:  # FIRES SECOND!
        for x in cycle((a, b)):
            x.b_set1wait2clear2()
            yield

    """
    @staticmethod
    @gpe_give_next
    def _template(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:
        pass
    """

    @staticmethod
    @gpe_give_next
    def receive_sync(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:
        for x in cycle((a, b)):
            x.b_set1wait2clear2()
            yield

    @staticmethod
    @gpe_give_next
    def send_sync(a: ProcessPairController, b: ProcessPairController) -> GPE_TYPE:
        for x in cycle((a, b)):
            x.b_set2wait1clear1()
            yield


PPC_PAIR_T = Tuple[ProcessPairController, ProcessPairController]


def ppc_pair() -> PPC_PAIR_T:
    return ProcessPairController(), ProcessPairController()


S_NONE = Union[str, None]
P_RECEIVER_TYPE = Generator[S_NONE, None, None]
CP_SENDER_TYPE = Callable[[S_NONE], bool]


class ConnectionTicket:
    _lock: Lock
    _id_connection_current: Value
    _id_connection_self: int

    def __init__(self):
        self._lock = Lock()
        self._id_connection_current = p_value(c_uint, 0, lock = Lock())
        self._id_connection_self = 0

    def __enter__(self):
        self._lock.__enter__()
        self._id_connection_current.value = self._id_connection_self

    def __exit__(self, *blah):
        self._lock.__exit__(*blah)

    @property
    def seat(self) -> int:
        return self._id_connection_self

    @property
    def servicing(self) -> int:
        return self._id_connection_current.value

    def next_idc(self) -> int:
        with (idc := self._id_connection_current).get_lock():
            self._id_connection_self = ni = idc.value
            idc.value += 1
            return ni


sp_error_state = namedtuple('sp_error_state', ('error_memory_sender', 'error_sending_sender', 'error_memory_receiver', 'error_sending_receiver'))


class SimplePipe:
    _pipe_send: Pipe
    _pipe_receive: Pipe
    _initiate_exchange: PPC_PAIR_T
    _sent_chunk: Event
    _got_chunk: Event
    _sent_a_none: Value
    _last_chunk: Value
    _fast_error: Value
    _e_memory_error_sender: Value
    _e_memory_error_receiver: Value
    _e_sending_failure_sender: Value
    _e_sending_failure_receiver: Value
    _receiver_g: Union[P_RECEIVER_TYPE, None]
    _sender_c: Union[CP_SENDER_TYPE, None]
    _chunk_size_start: int
    _encoding: str
    _connection_ticket: ConnectionTicket

    def __init__(self, chunk_size_start: int = 10_000, encoding: str = 'UTF-8'):
        self._pipe_receive, self._pipe_send = Pipe(True)
        self._initiate_exchange = ppc_pair()
        self._sent_chunk = Event()
        self._got_chunk = Event()
        self._sent_a_none = p_value(c_bool, False)
        self._last_chunk = p_value(c_bool, False)
        self._fast_error = p_value(c_bool, False)
        self._e_memory_error_sender = p_value(c_bool, False)
        self._e_memory_error_receiver = p_value(c_bool, False)
        self._e_sending_failure_sender = p_value(c_bool, False)
        self._e_sending_failure_receiver = p_value(c_bool, False)
        self._receiver_g = self._sender_c = None
        self._chunk_size_start = chunk_size_start  # ~32MillionBytes Pipe() limit
        self._encoding = encoding
        self._connection_ticket = ConnectionTicket()  # connection facilitation

    def init_sender(self):
        def sender(i: S_NONE) -> bool:
            return sender_g.send(i)

        self._sender_c = sender
        next(sender_g := self._send_data())  # I <3 WALRUS OPERATOR!

    def init_receiver(self):
        self._receiver_g = rg = self._receive_data()
        next(rg)  # # pre-initialization

    def __del__(self):
        for pipe in self._pipe_receive, self._pipe_send:
            if not pipe.closed:
                pipe.close()

    @property
    def receiver(self) -> P_RECEIVER_TYPE:
        return self._receiver_g

    @property
    def sender(self) -> CP_SENDER_TYPE:
        return self._sender_c

    @property
    def connection_locker(self) -> ConnectionTicket:
        return self._connection_ticket

    def set_id(self) -> int:
        return self._connection_ticket.next_idc()

    def _send_data(self) -> Generator[bool, S_NONE, None]:  # SENT SENDER SENDS!
        p_send = self._pipe_send
        sent_chunk = self._sent_chunk
        got_chunk = self._got_chunk
        sent_a_none = self._sent_a_none
        last_chunk = self._last_chunk
        fast_error = self._fast_error
        memory_error = self._e_memory_error_sender
        sending_failure = self._e_sending_failure_sender
        start_chunk_size = self._chunk_size_start
        text_encoding = self._encoding

        id_ps = get_ps_id(True, False)
        initiate_exchange = GeneratePPCExchange.send_sync(*self._initiate_exchange)

        def switch_on_error(trip_this: Exception):
            (memory_error if isinstance(trip_this, MemoryError) else sending_failure).value = fast_error.value = True

        while True:  #
            data_to_send = (yield fast_error.value)
            sent_a_none.value = din = data_to_send is None
            initiate_exchange()  # Loop start
            memory_error.value = sending_failure.value = fast_error.value = False  # clear error flags
            last_chunk.value = False
            if din:
                continue
            b_data = b''
            bd_index = 0
            try:
                b_data = str.encode(data_to_send, text_encoding)
            except (MemoryError, UnicodeEncodeError) as encoding_error:
                switch_on_error(encoding_error)
            bd_length = len(b_data)
            initiate_exchange()  # Load string
            if fast_error.value:
                continue
            chunk_size_attempt = start_chunk_size
            while True:
                if bd_index + chunk_size_attempt >= bd_length:
                    chunk_size = bd_length - bd_index
                    last_chunk.value = True
                else:
                    chunk_size = chunk_size_attempt
                try:
                    p_send.send_bytes(b_data, bd_index, chunk_size)
                    bd_index += chunk_size
                except (ValueError, MemoryError) as send_error:
                    switch_on_error(send_error)
                sent_chunk.set()
                event_wait_clear(got_chunk)
                if last_chunk.value:
                    break
                if fast_error.value:
                    if chunk_size_attempt > 1:
                        chunk_size_attempt >>= 1
                    else:
                        last_chunk.value = True

    def _receive_data(self) -> P_RECEIVER_TYPE:  # RECEIVED RECEIVER RECEIVES!
        p_receive = self._pipe_receive
        sent_chunk = self._sent_chunk
        got_chunk = self._got_chunk
        sent_a_none = self._sent_a_none
        last_chunk = self._last_chunk
        fast_error = self._fast_error
        memory_error = self._e_memory_error_receiver
        sending_failure = self._e_sending_failure_receiver
        text_encoding = self._encoding

        id_ps = get_ps_id(False, False)
        aggregator = BytesIO()
        initiate_exchange = GeneratePPCExchange.receive_sync(*self._initiate_exchange)

        def switch_on_error(trip_this: Exception):
            (memory_error if isinstance(trip_this, MemoryError) else sending_failure).value = fast_error.value = True

        yield  # pre-initialization
        while True:  #
            initiate_exchange()  # Loop start
            memory_error.value = sending_failure.value = False  # clear error flags
            if sent_a_none.value:
                yield None
                continue
            initiate_exchange()  # Load string
            if fast_error.value:
                continue
            while True:
                event_wait_clear(sent_chunk)
                if p_receive.poll():
                    try:
                        aggregator.write(p_receive.recv_bytes())
                    except (MemoryError, EOFError, IOError) as read_error:
                        switch_on_error(read_error)
                got_chunk.set()
                if last_chunk.value:
                    break
            try:
                place = aggregator.tell()
                aggregator.seek(0)
                yield aggregator.read(place).decode(text_encoding)
            except (MemoryError, EOFError, IOError, UnicodeDecodeError) as decode_error:
                switch_on_error(decode_error)
                yield ''
            aggregator.seek(0)

    @property
    def text_encoding(self) -> str:
        return self._encoding

    @property
    def memory_error_sender(self) -> bool:
        return self._e_memory_error_sender.value

    @property
    def sending_failure_sender(self) -> bool:
        return self._e_sending_failure_sender.value

    @property
    def memory_error_receiver(self) -> bool:
        return self._e_memory_error_receiver.value

    @property
    def sending_failure_receiver(self) -> bool:
        return self._e_sending_failure_receiver.value

    @property
    def error(self) -> bool:
        return any((self._e_memory_error_sender.value, self._e_sending_failure_sender.value,
                    self._e_memory_error_receiver.value, self._e_sending_failure_receiver.value))

    @property
    def sending_error(self) -> bool:
        return self._e_memory_error_sender.value or self._e_sending_failure_sender.value

    @property
    def receiving_error(self) -> bool:
        return self._e_memory_error_receiver.value or self._e_sending_failure_receiver.value

    def ask_error_state(self) -> sp_error_state:
        return sp_error_state(
            self._e_memory_error_sender.value, self._e_sending_failure_sender.value,
            self._e_memory_error_receiver.value, self._e_sending_failure_receiver.value)

    def ask_error_state_string(self) -> str:
        return ''.join(('T' if x else 'F') for x in self.ask_error_state())


print_text_lock = Lock()


def get_ps_id(sender: bool, tester: bool) -> str:
    return ('Sender.Test:' if tester else 'Sender.Pipe:') if sender else ('Receiver.Test:' if tester else 'Receiver.Pipe:')


def print_safe(sender_message: str, *args, **kwargs):
    with print_text_lock:
        print(sender_message, *args, **kwargs)


def get_input(msg: str) -> str:
    with print_text_lock:
        return input(msg)


def sp_main():
    nexis = SimplePipe()

    def f_input():
        nexis.init_sender()
        d_send = nexis.sender
        quit_phrases = ('quit', 'end', 'none')
        id_ps = get_ps_id(True, True)
        while True:
            try:
                error = d_send(d_in := (None if (d_in := get_input('Message: ')).strip().lower() in quit_phrases else d_in))  # I <3 WALRUS OPERATOR!
            except EOFError:  # input
                continue
            if error:
                print_safe(id_ps, f'Error while sending {repr(d_in)} with error state {nexis.ask_error_state_string()}.')
                continue
            if d_in is None:
                break
        print_safe(id_ps, 'Session ended.')

    def f_print():
        nexis.init_receiver()
        d_receive = nexis.receiver
        id_ps = get_ps_id(False, True)
        print_safe(id_ps, 'Initializing.')
        while True:
            try:
                print_safe(id_ps, 'Receiving data...')
                text = next(d_receive)
                print_safe(id_ps, 'Message compiled.')
                if nexis.error:
                    print_safe(id_ps, 'Error state', nexis.ask_error_state_string(), 'encountered.')
            except MemoryError:
                print_safe(id_ps, 'Error rejoining test.')
                continue
            if text is None:
                print_safe(id_ps, 'Output = None.')
                break
            else:
                print_safe(id_ps, f'Output: "{text}";')
        print_safe(id_ps, 'Session concluded.')

    (p_print := Process(target = f_print, name = "P_print")).start()
    f_input()
    p_print.join()
    return


if __name__ == '__main__':
    sp_main()

# Test

