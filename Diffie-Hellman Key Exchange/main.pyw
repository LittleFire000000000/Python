#!/usr/bin/python3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *

from threading import Thread, Lock, local

from webbrowser import open_new_tab
from math import floor, sqrt, log
from secrets import randbits, randbelow

title = "Diffie-Hellman Key Exchange"


#
def better_isqrt(i: int) -> int :  # Vedic Square Root Algorithm
    """
    Implement the Vedic Square Root Algorithm.
    It's slower than math.sqrt(), but it's accurate.
    :param i: whole number
    :return: whole number
    """
    x0 = str(i)
    if len(x0) % 2 : x0 = '0' + x0
    #
    divisor = 0
    dropped = 0
    bases = '0'
    #
    for y0 in range(0, len(x0), 2) :
        dropped = int(str(dropped) + x0[y0 :y0 + 2])
        affixed = 1
        tmp = 0
        while True :
            y1 = (divisor * 10 + affixed) * affixed
            if y1 > dropped :
                affixed -= 1
                y1 = tmp
                break
            affixed += 1
            tmp = y1
        dropped -= y1
        bases += str(affixed)
        divisor = int(bases) * 2
    #
    return int(bases)


#

class Collection :
    __single_fxn = None
    __dictionary = {}
    __disciples = []
    
    def __init__(self, single_fxn, *args, **kwargs) :
        self.__single_fxn = single_fxn
        self.__dictionary = kwargs
        self.__disciples = list(args)
    
    def add(self, obj) :
        self.__dictionary[obj.get_name()] = obj.BLANK
        self.__disciples.append(obj)
    
    def link(self) :
        for x in self.__disciples : x.link()
    
    def lock(self) :
        for x in self.__disciples : x.lock()
    
    def unlock(self) :
        for x in self.__disciples : x.unlock()
    
    def get(self) :
        return self.__dictionary
    
    def call(self) :
        return self.__single_fxn()
    
    def obj_dict_set(self, obj, value) :
        self.__dictionary[obj.get_name()] = value
        if not self.__single_fxn is None : self.call()
    
    def send(self, obj, value) :
        if not obj.is_locked() : self.obj_dict_set(obj, value)
        for x in self.__disciples : x.setter(True)
        for x in self.__disciples : x.setter(False)


class InterStringEntry(Entry) :
    __variable = None
    
    def __init__(self, master=None, widget=None, **kw) :
        Entry.__init__(self, master=master, widget=widget, **kw)
        a = kw.get('textvariable')
        if not a is None :
            self.__variable = a
    
    def get_string_var(self) :
        return self.__variable
    
    def configure(self, cnf=None, **kw) :
        if 'state' in kw and not self.__variable is None :
            if kw['state'] == DISABLED :
                self.__variable.lock()
            elif kw['state'] == ACTIVE :
                self.__variable.unlock()
            del kw['state']
        Entry.configure(self, cnf, **kw)


class InterStringCheckbutton(Checkbutton) :
    __variable = None
    
    def __init__(self, master=None, widget=None, **kw) :
        super().__init__(master, **kw)
        Checkbutton.__init__(self, master=master, widget=widget, **kw)
        a = kw.get('variable')
        if not a is None :
            self.__variable = a
    
    def get_boolean_var(self) :
        return self.__variable
    
    def configure(self, cnf=None, **kw) :
        if 'state' in kw and not self.__variable is None :
            if kw['state'] == DISABLED :
                self.__variable.lock()
            elif kw['state'] == ACTIVE :
                self.__variable.unlock()
        Checkbutton.configure(self, cnf, **kw)


class InterStringVar(StringVar) :
    __collection = None
    __function = None
    __named = None
    __form = None
    __lock = False
    
    BLANK = ''
    
    def __init__(self, collection: Collection, function, name: str, form: str, **kwargs) :
        StringVar.__init__(self, **kwargs)
        self.__collection = collection
        self.__function = function
        self.__named = name
        self.__form = form
        collection.add(self)
    
    def get_name(self) :
        return self.__named
    
    def get_collection(self) :
        return self.__collection
    
    def set(self, value) :
        self.__collection.send(self, value)
    
    def setter(self, first_pass: bool) :
        if first_pass :
            if not self.__function is None :
                self.__function()
        else :
            StringVar.set(self, self.__form.format(**self.__collection.get()))
    
    def update(self, *_) :
        if not self.is_locked() : self.__collection.obj_dict_set(self, self.get())
        self.setter(True)
        self.setter(False)
    
    def link(self) :
        self.trace_variable('w', self.update)
    
    def is_locked(self) :
        return self.__lock
    
    def lock(self) :
        self.__lock = True
    
    def unlock(self) :
        self.__lock = False


class InterBooleanVar(BooleanVar) :
    __collection = None
    __function = None
    __named = None
    __lock = False
    
    BLANK = False
    
    def __init__(self, collection: Collection, function, name: str, **kwargs) :
        BooleanVar.__init__(self, **kwargs)
        self.__collection = collection
        self.__function = function
        self.__named = name
        collection.add(self)
    
    def get_name(self) :
        return self.__named
    
    def get_collection(self) :
        return self.__collection
    
    def set(self, value) :
        self.__collection.send(self, value)
    
    def setter(self, first_pass: bool) :
        if first_pass :
            BooleanVar.set(self, self.__collection.get()[self.__named])
        else :
            if not self.__function is None : self.__function()
    
    def update(self, *_) :
        if not self.is_locked() : self.__collection.obj_dict_set(self, self.get())
        self.setter(True)
        self.setter(False)
    
    def link(self) :
        self.trace_variable('w', self.update)
    
    def is_locked(self) :
        return self.__lock
    
    def lock(self) :
        self.__lock = True
    
    def unlock(self) :
        self.__lock = False


#


def scramble(x: int) -> list :
    y = list(reversed(range(x)))
    for z in range(x) :
        z1 = randbelow(x)
        y[z], y[z1] = y[z1], y[z]
    return y


#

def is_power2(x: int) -> bool :
    y = bin(x)[2 :]
    if y[0] == '0' : return False
    for z in y[1 :] :
        if z == '1' : return False
    return True


#

class Characters :
    VALUES: str = '!"#$%&\'()*,./0123456789:;<>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    LEN: int = len(VALUES)
    LEN_SQRT: int = floor(sqrt(LEN))
    
    BIT_COUNT_MIN: int = 2048
    BIT_COUNT_MIN_ROOT: int = 11
    BIT_COUNT: int = BIT_COUNT_MIN
    BIT_COUNT_ROOT: int = BIT_COUNT_MIN_ROOT
    
    @classmethod
    def class_get_power_minimum(cls) -> int :
        return cls.BIT_COUNT_MIN_ROOT
    
    @classmethod
    def class_get_power(cls) -> int :
        return cls.BIT_COUNT_ROOT
    
    @classmethod
    def class_set_power(cls, x: int) :
        assert x >= cls.BIT_COUNT_MIN_ROOT, "The minimum is power " + str(cls.BIT_COUNT_MIN_ROOT) + "."
        cls.BIT_COUNT = 2 ** x
        cls.BIT_COUNT_ROOT = x
    
    @classmethod
    def class_get_bit_count_minimum(cls) -> int :
        return cls.BIT_COUNT_MIN
    
    @classmethod
    def class_get_bit_count(cls) -> int :
        return cls.BIT_COUNT
    
    @classmethod
    def class_set_bit_count(cls, x: int, y: int) :
        assert x >= cls.BIT_COUNT_MIN, "The minimum is bit_count " + str(cls.BIT_COUNT_MIN) + "."
        assert 2 ** y == x, "Invalid base."
        cls.BIT_COUNT = x
        cls.BIT_COUNT_ROOT = y
    
    def __init__(self, tf: bool) :
        self.reset_dict(tf)
    
    def in_dict(self, x: str) -> bool :
        return x in self.__dictionary.keys()
    
    def get_dict(self) :
        return self.__dictionary.copy()
    
    def get_dict_key(self, x: str) :
        return self.__dictionary[x]
    
    def set_dict_key(self, x: str, y: bool) :
        self.__dictionary[x] = y
    
    def reset_dict(self, tf: bool) :
        self.__dictionary = {a : tf for a in Characters.VALUES}
        self.__string = ''
    
    def get_string(self) -> str :
        return self.__string
    
    def get_number(self) -> int :
        return self.__number
    
    def set_string(self, x: str) :
        self.__string = x
        self.__number = None
    
    def set_number(self, x: int) :
        assert x >= 0
        self.__number = x
    
    def fit_str(self, x: str) -> bool :
        self.set_string(x)
        for y in x :
            if not self.in_dict(y) : return False
        return True
    
    def fit_str_on(self, x: str) -> bool :
        if self.fit_str(x) :
            for y in x :
                if not self.get_dict_key(y) : return False
            return True
        return False
    
    def fit_str_enhanced(self, x: str) -> str :
        tmp = ''
        for y in x :
            if self.in_dict(y) :
                if self.get_dict_key(y) : tmp += y
        return tmp
    
    def __numbered(self) :
        self.tmp_STR: tuple[str] = tuple(sorted(x for x, y in self.__dictionary.items() if y))
        self.tmp_LEN: int = len(self.tmp_STR)
    
    def gen_number(self) :
        self.__numbered()
        self.__number = 0
        for i in self.__string :
            self.__number *= self.tmp_LEN
            self.__number += self.tmp_STR.index(i)
    
    def gen_string(self) :
        self.__numbered()
        self.__string: str = ''
        tmp = self.__number
        while True :
            self.__string: str = self.tmp_STR[tmp % self.tmp_LEN] + self.__string
            tmp //= self.tmp_LEN
            if not tmp : break


#


class CharCross :
    cls = None
    x: str = ''
    
    __check: InterStringCheckbutton = None
    __check_vars: dict = None
    
    def __init__(self, cls, x1: str) :
        self.cls = cls
        self.x = x1
    
    def char_cross(self, button: InterStringCheckbutton, variable: dict) :
        self.__check = button
        self.__check_vars = variable
        #
        self.__check.bind('<Enter>', lambda _ : self._focus_setter())
        self.__check.bind('<Key>', lambda eve : self._key_press(eve.char))
    
    def _focus_setter(self) :
        if not self.__check.get_boolean_var().is_locked() :
            self.__check.focus_set()
    
    def _key_press(self, x: str) :
        if not self.__check.get_boolean_var().is_locked() :
            if x in self.__check_vars.keys() :
                p = self.__check_vars[x]
                p.focus_set()
                p.get_boolean_var().set(not p.get_boolean_var().get())
    
    def __call__(self, *args, **kwargs) :
        self.cls.characters.set_dict_key(self.x, self.cls.character_set.get()[self.x])


class DH :
    def __init__(self) :
        self.characters = Characters(False)
    
    def state_buttons_entry(self, x, state: str, exceptions: set = set()) :
        for y in x.winfo_children() :
            if not y in exceptions :
                if isinstance(y, (InterStringEntry, Button, Checkbutton)) :
                    y.configure(state=state)
                elif isinstance(y, (Frame, LabelFrame)) :
                    self.state_buttons_entry(y, state, exceptions)
    
    def load(self) :
        self.tk_window = Tk()
        self.tk_window.wm_title(title)
        
        #
        self.collection = Collection(None)
        self.FONT = ('TNR', 73, 'bold')
        
        def flr(obj: DH, name) :
            tmp = ''
            for x2 in obj.collection.get()[name] :
                if self.characters.in_dict(x2) :
                    if self.characters.get_dict_key(x2) :  tmp += x2
            obj.collection.get()[name] = tmp
        
        self.seed = InterStringVar(self.collection, lambda : flr(self, 'seed'), 'seed', '{seed}')
        self.prime_modulus = InterStringVar(self.collection, lambda : flr(self, 'prime'), 'prime', '{prime}')
        
        #
        self.prime_modulus_processing = False
        self.prime_modulus_try_count = 0
        
        def prime_modulus_processing() :
            if self.prime_modulus_processing :
                self.collection.get()['prime_processing_tmp'] = (
                        '\nIN PROGRESS' + (
                    ' ({})'.format(str(self.prime_modulus_try_count)) if self.prime_modulus_try_count else ''))
            else :
                self.collection.get()['prime_processing_tmp'] = ''
        
        self.prime_modulus_message = InterStringVar(self.collection, prime_modulus_processing, 'prime_processing',
                                                    'Verify Prime Modulus as Prime{prime_processing_tmp}')
        
        #
        self.generator_processing = False
        self.generator_try_count = 0
        
        def generator_processing() :
            if self.generator_processing :
                self.collection.get()['generator_processing_tmp'] = (
                        '\nIN PROGRESS' + (
                    ' ({}%)'.format(str(self.generator_try_count)) if self.generator_try_count else ''))
            else :
                self.collection.get()['generator_processing_tmp'] = ''
        
        self.generator_message = InterStringVar(self.collection, generator_processing, 'generator_processing',
                                                'Derive the floor-root Generator{generator_processing_tmp}')
        
        #
        self.generator = InterStringVar(self.collection, lambda : flr(self, 'gen'), 'gen', '{gen}')
        self.exchange_frame_reminder_variable = InterStringVar(self.collection, None, 'bob_alice', '{bob_alice}')
        self.exchange_frame_alice_value = InterStringVar(self.collection, lambda : flr(self, 'alice'), 'alice',
                                                         '{alice}')
        self.exchange_frame_bob_value = InterStringVar(self.collection, lambda : flr(self, 'bob'), 'bob', '{bob}')
        
        def msg() :
            self.collection.get()['result_tmp'] = \
                {"Neither" : "", "Alice" : " from Bob", "Bob" : " from Alice"}.get(self.collection.get()['bob_alice'],
                                                                                   '')
        
        self.final_frame_message = InterStringVar(self.collection, msg, 'result',
                                                  'Take the Received Number{result_tmp} and raise it to Your Private Number')
        self.final_frame_value = InterStringVar(self.collection, lambda : flr(self, 'result_final'), 'result_final',
                                                '{result_final}')
        
        self.collection.link()
        
        #
        self.window_frame = Frame(self.tk_window)
        self.window_frame.grid(column=0, row=0, sticky=NSEW)
        
        self.window_manuel = Frame(self.window_frame)
        self.window_manuel.grid(column=0, row=0, sticky=NSEW)
        
        self.window_automatic = Frame(self.window_frame)
        self.window_automatic.grid(column=0, row=0, sticky=NSEW)
        
        self.window_main = Frame(self.window_frame)
        self.window_main.grid(column=0, row=0, sticky=NSEW)
        
        Grid.columnconfigure(self.window_frame, 0, weight=1)
        Grid.rowconfigure(self.window_frame, 0, weight=1)
        
        #
        self.window_up_label = Label(self.window_manuel, text=title, font=self.FONT)
        self.window_up_label.grid(column=0, row=0, sticky=EW)
        
        self.window_up = Frame(self.window_manuel)
        self.window_up.grid(column=0, row=1, sticky=NSEW)
        
        self.window_right = LabelFrame(self.window_up, text="Tool Controls")
        self.window_right.grid(column=0, row=0)
        
        self.window1 = LabelFrame(self.window_right, text="Step 0A - Character Set")
        self.window1.grid(column=0, row=0)
        
        self.character_set_label = Label(self.window1,
                                         text="All of the numbers in the procedure are encoded with this set of characters.")
        self.character_set_label.pack()
        
        self.character_set_box_frame = Frame(self.window1)
        self.character_set_box_frame.pack()
        
        self.character_set_box_frame1 = Frame(self.character_set_box_frame)
        self.character_set_box_frame1.pack()
        
        self.character_set_boxes = {}
        self.character_set_variables = {}
        self.character_set = Collection(None)
        
        for i, x in enumerate(Characters.VALUES) :
            a = CharCross(self, x)
            y = InterBooleanVar(self.character_set, a, x)
            self.character_set_variables[x] = y
            z0 = InterStringCheckbutton(self.character_set_box_frame1, text=x, variable=y)
            z0.grid(row=i % Characters.LEN_SQRT, column=i // Characters.LEN_SQRT)
            self.character_set_boxes[x] = z0
            a.char_cross(z0, self.character_set_boxes)
        
        self.character_set.link()
        
        def select(all_none: (bool, None)) :
            if all_none is None :
                y0 = True
                y1 = set()
                z1 = len(Characters.VALUES)
                while y0 :
                    for x0 in scramble(z1) :
                        if len(y1) == Characters.LEN_SQRT :
                            y0 = False
                            break
                        if (randbits(3) - 1) % 2 : y1.add(x0)
                for x0 in y1 :
                    x0 = self.character_set_variables[Characters.VALUES[x0]]
                    if not x0.get() :
                        BooleanVar.set(x0, True)
                        self.character_set.obj_dict_set(x0, True)
                self.character_set_box_frame_setter_button_lock.focus_set()
            else :
                for obj_x in self.character_set_variables.values() :
                    if obj_x.get() ^ all_none :
                        BooleanVar.set(obj_x, all_none)
                        self.character_set.obj_dict_set(obj_x, all_none)
                if all_none :
                    self.character_set_box_frame_setter_button_lock.focus_set()
                else :
                    self.character_set_box_frame_setter_button_random.focus_set()
        
        self.character_set_box_frame_setter_frame = Frame(self.character_set_box_frame)
        self.character_set_box_frame_setter_frame.pack()
        
        def lock_0a() :
            if not sum(1 if x1.get() else 0 for x1 in self.character_set_variables.values()) >= Characters.LEN_SQRT :
                showerror(title, "At least {} characters must be selected.".format(Characters.LEN_SQRT))
                while True :
                    a0 = Characters.VALUES[randbelow(Characters.LEN)]
                    if not self.character_set_variables[a0].get() : break
                self.character_set_boxes[a0].focus_set()
                return
            self.state_buttons_entry(self.character_set_box_frame, DISABLED)
            #
            self.characters.set_number(Characters.class_get_bit_count_minimum())
            self.characters.gen_string()
            self.bit_length_set.get()['value_str_tmp'] = self.characters.get_string()
            StringVar.set(self.bit_length_set_value_value, self.characters.get_string())
            #
            self.characters.set_number(Characters.class_get_power_minimum())
            self.characters.gen_string()
            self.bit_length_set.get()['power_str_tmp'] = self.characters.get_string()
            StringVar.set(self.bit_length_set_value_power, self.characters.get_string())
            #
            unlock_0b()
            self.window_up_frame_button.configure(state=DISABLED)
            self.window2_base_10_variable.set('0')
            self.window2_base_10_frame_entry.focus_set()
        
        self.character_set_box_frame_setter_button_lock = Button(self.character_set_box_frame_setter_frame,
                                                                 text="Lock", command=lock_0a)
        self.character_set_box_frame_setter_button_lock.pack(side=LEFT)
        
        self.character_set_box_frame_setter_button_random = Button(self.character_set_box_frame_setter_frame,
                                                                   text="Random " + str(Characters.LEN_SQRT),
                                                                   command=lambda : select(None))
        self.character_set_box_frame_setter_button_random.pack(side=LEFT)
        
        self.character_set_box_frame_setter_button_all = Button(self.character_set_box_frame_setter_frame,
                                                                text="Select All", command=lambda : select(True))
        self.character_set_box_frame_setter_button_all.pack(side=LEFT)
        
        self.character_set_box_frame_setter_button_none = Button(self.character_set_box_frame_setter_frame,
                                                                 text="Select None", command=lambda : select(False))
        self.character_set_box_frame_setter_button_none.pack(side=LEFT)
        
        #
        self.window2 = LabelFrame(self.window_right, text="Step 0B - Convert To&Fro Digits")
        self.window2.grid(column=0, row=1)
        
        self.window2_label = Label(self.window2, text="Convert base-10 numbers into the current obscure character-set.")
        self.window2_label.pack()
        
        def base_fro_10() :
            if self.lock.acquire(False) :
                if not self.window2_base_10_variable.is_locked() :
                    a0: str = self.window2_collection.get()['b10']
                    if a0 == '' : a0 = '0'
                    if a0.isdigit() :
                        self.window2_collection.get()['b10_tmp'] = a0
                        self.characters.set_number(int(a0))
                        self.characters.gen_string()
                        self.window2_collection.get()['b_o_tmp'] = self.characters.get_string()
                        self.window2_base_obscure_variable.setter(False)
                    self.lock.release()
        
        def base_fro_obscure() :
            if not self.window2_base_10_variable.is_locked() :
                if self.lock.acquire(False) :
                    a0: str = self.window2_collection.get()['b_o']
                    if self.characters.fit_str_on(a0) :
                        self.window2_collection.get()['b_o_tmp'] = self.characters.get_string()
                        self.characters.gen_number()
                        self.window2_collection.get()['b10_tmp'] = str(self.characters.get_number())
                        self.window2_base_10_variable.setter(False)
                    self.lock.release()
        
        self.window2_collection = Collection(None)
        self.window2_base_10_variable = InterStringVar(self.window2_collection, base_fro_10, 'b10', '{b10_tmp}')
        self.window2_base_obscure_variable = InterStringVar(self.window2_collection, base_fro_obscure, 'b_o',
                                                            '{b_o_tmp}')
        self.window2_collection.link()
        
        self.window2_collection.get()['b10_tmp'] = InterStringVar.BLANK
        self.window2_collection.get()['b_o_tmp'] = InterStringVar.BLANK
        
        def w2_up_down(up: bool) :
            if self.lock.acquire(False) :
                if self.window2_base_10_variable.is_locked() :
                    self.lock.release()
                    return
                a0 = int(self.window2_base_10_variable.get())
                if up :
                    a0 += 1
                elif a0 > 0 :
                    a0 -= 1
                self.window2_base_10_variable.set(str(a0))
                self.lock.release()
        
        self.window2_base_10_frame = Frame(self.window2)
        self.window2_base_10_frame.pack()
        
        self.window2_base_10_frame_label = Label(self.window2_base_10_frame, text="Base-10 Number:")
        self.window2_base_10_frame_label.pack(side=LEFT)
        
        self.window2_base_10_frame_entry = InterStringEntry(self.window2_base_10_frame,
                                                            textvariable=self.window2_base_10_variable)
        self.window2_base_10_frame_entry.pack(side=LEFT)
        
        self.window2_base_10_frame_entry.bind('<Up>', lambda _ : w2_up_down(True))
        self.window2_base_10_frame_entry.bind('<Down>', lambda _ : w2_up_down(False))
        
        self.window2_base_obscure_frame = Frame(self.window2)
        self.window2_base_obscure_frame.pack()
        
        self.window2_base_obscure_frame_label = Label(self.window2_base_obscure_frame, text="Obscure-base Number:")
        self.window2_base_obscure_frame_label.pack(side=LEFT)
        
        self.window2_base_obscure_frame_entry = InterStringEntry(self.window2_base_obscure_frame,
                                                                 textvariable=self.window2_base_obscure_variable)
        self.window2_base_obscure_frame_entry.pack(side=LEFT)
        
        self.window2_base_obscure_frame_entry.bind('<Up>', lambda _ : w2_up_down(True))
        self.window2_base_obscure_frame_entry.bind('<Down>', lambda _ : w2_up_down(False))
        
        def lock_0b(z1: bool) :
            self.state_buttons_entry(self.window2, DISABLED,
                                     {self.window2_unlock} if ((not self.window2_unlocked) and z1) else set())
            if z1 and not self.window2_unlocked :
                self.window2_unlocked = True
                self.bit_length_set_entry_power.focus_set()
                unlock_0c()
            elif self.window2_unlocked :
                self.window2_unlock.configure(state=ACTIVE)
                self.window2_base_10_frame_entry.focus_set()
        
        def unlock_0b() :
            self.state_buttons_entry(self.window2, ACTIVE)
            self.window2_base_10_frame_entry.focus_set()
        
        self.window2_lock_frame = Frame(self.window2)
        self.window2_lock_frame.pack()
        
        self.window2_lock = Button(self.window2_lock_frame, text="Lock", command=lambda : lock_0b(True))
        self.window2_lock.pack(side=LEFT)
        
        self.window2_unlocked = False
        self.window2_unlock = Button(self.window2_lock_frame, text="Unlock", command=unlock_0b)
        self.window2_unlock.pack(side=LEFT)
        
        lock_0b(False)
        
        #
        self.window3 = LabelFrame(self.window_right, text="Step 0C - Key Bit-Length")
        self.window3.grid(column=0, row=2)
        
        self.bit_length_label = Label(self.window3, text="How many bits in final key")
        self.bit_length_label.pack()
        
        def bit_set(z1: (None, bool), zoe: bool) :
            if zoe :
                if not self.bit_length_set_value_power.is_locked() :
                    if z1 :  # power
                        if self.characters.fit_str_on(self.bit_length_set.get()['power']) :
                            self.bit_length_set.get()['power_str_tmp'] = self.characters.get_string()
                            self.characters.gen_number()
                            if self.characters.get_number() >= Characters.class_get_power_minimum() :
                                self.characters.set_number(2 ** self.characters.get_number())
                                self.characters.gen_string()
                                z1 = self.characters.get_string()
                                self.bit_length_set.get()['value_str_tmp'] = z1
                                self.bit_length_set_value_value.setter(False)
                        else :
                            self.bit_length_set.get()['power_str_tmp'] = self.characters.fit_str_enhanced(
                                self.bit_length_set.get()['power'])
                    else :  # value
                        if self.characters.fit_str_on(self.bit_length_set.get()['value']) :
                            self.characters.gen_number()
                            if self.characters.get_number() >= Characters.class_get_bit_count_minimum() :
                                self.bit_length_set.get()['value_str_tmp'] = self.characters.get_string()
                                if is_power2(self.characters.get_number()) :
                                    self.characters.set_number(int(log(self.characters.get_number(), 2)))
                                    self.characters.gen_string()
                                    StringVar.set(self.bit_length_set_value_power, self.characters.get_string())
                                    self.bit_length_set_value_power.setter(False)
                        else :
                            self.bit_length_set.get()['value_str_tmp'] = self.characters.fit_str_enhanced(
                                self.bit_length_set.get()['value'])
            else :  # init
                self.bit_length_set.get()['power_str_tmp'] = InterStringVar.BLANK
                self.bit_length_set.get()['value_str_tmp'] = InterStringVar.BLANK
        
        self.bit_length_set = Collection(None)
        self.bit_length_set_value_power = InterStringVar(self.bit_length_set, lambda : bit_set(True, True), 'power',
                                                         '{power_str_tmp}')
        self.bit_length_set_value_value = InterStringVar(self.bit_length_set, lambda : bit_set(False, True), 'value',
                                                         '{value_str_tmp}')
        self.bit_length_set.link()
        
        bit_set(None, False)
        
        self.bit_length_set_frame = Frame(self.window3)
        self.bit_length_set_frame.pack()
        
        def ascend_descend(x0: bool) :
            if not self.bit_length_set_value_power.is_locked() :
                self.characters.set_string(self.bit_length_set_value_power.get())
                self.characters.gen_number()
                if self.characters.get_number() >= self.characters.class_get_power_minimum() and x0 :
                    self.characters.set_number(self.characters.get_number() + 1)
                elif self.characters.get_number() > self.characters.class_get_power_minimum() and not x0 :
                    self.characters.set_number(self.characters.get_number() - 1)
                self.characters.gen_string()
                self.bit_length_set_value_power.set(self.characters.get_string())
        
        self.bit_length_set_frame_power = Frame(self.bit_length_set_frame)
        self.bit_length_set_frame_power.pack()
        
        self.bit_length_set_label_power = Label(self.bit_length_set_frame_power, text="Power:")
        self.bit_length_set_label_power.pack(side=LEFT)
        
        self.bit_length_set_entry_power = InterStringEntry(self.bit_length_set_frame_power,
                                                           textvariable=self.bit_length_set_value_power)
        self.bit_length_set_entry_power.pack(side=LEFT)
        
        self.bit_length_set_entry_power.bind('<Up>', lambda _ : ascend_descend(True))
        self.bit_length_set_entry_power.bind('<Down>', lambda _ : ascend_descend(False))
        
        self.bit_length_set_frame_value = Frame(self.bit_length_set_frame)
        self.bit_length_set_frame_value.pack()
        
        self.bit_length_set_label_value = Label(self.bit_length_set_frame_value, text="Value:")
        self.bit_length_set_label_value.pack(side=LEFT)
        
        self.bit_length_set_entry_value = InterStringEntry(self.bit_length_set_frame_value,
                                                           textvariable=self.bit_length_set_value_value)
        self.bit_length_set_entry_value.pack(side=LEFT)
        
        self.bit_length_set_entry_value.bind('<Up>', lambda _ : ascend_descend(True))
        self.bit_length_set_entry_value.bind('<Down>', lambda _ : ascend_descend(False))
        
        self.bit_length_set_button_frame = Frame(self.window3)
        self.bit_length_set_button_frame.pack()
        
        def lock_0c(z: bool) :
            self.state_buttons_entry(self.window3, DISABLED)
            if z :
                self.seed_box_entry.focus_set()
                unlock_1()
        
        def unlock_0c() :
            self.state_buttons_entry(self.window3, ACTIVE)
        
        def locker_0c() :
            self.characters.set_string(self.bit_length_set_value_power.get())
            self.characters.gen_number()
            a0 = self.characters.get_number()
            self.characters.set_string(self.bit_length_set_value_value.get())
            self.characters.gen_number()
            a1 = self.characters.get_number()
            #
            if 2 ** a0 == a1 :
                Characters.class_set_power(a0)
                Characters.class_set_bit_count(a1, a0)
                lock_0c(True)
            else :
                showerror(title, "The Value must be two raised to the Root.")
        
        self.bit_length_set_button_button = Button(self.bit_length_set_button_frame, text="Lock", command=locker_0c)
        self.bit_length_set_button_button.pack()
        
        lock_0c(False)
        
        #
        self.window = LabelFrame(self.window_up, text="Procedure")
        self.window.grid(column=1, row=0)
        
        #
        self.window_frame1 = Frame(self.window)
        self.window_frame1.grid(column=0)
        
        self.seed_frame = LabelFrame(self.window_frame1, text="Step 1")
        self.seed_frame.pack(side=LEFT)
        self.seed_label = Label(self.seed_frame, text="Seed the Generation of a Prime Modulus")
        self.seed_label.pack(side=TOP)
        self.seed_box_entry = InterStringEntry(self.seed_frame, textvariable=self.seed)
        self.seed_box_entry.pack()
        
        self.seed_box_frame0 = Frame(self.seed_frame)
        self.seed_box_frame0.pack()
        self.seed_box_frame = Frame(self.seed_box_frame0)
        self.seed_box_frame.pack()
        
        def randomise() :
            self.characters.set_number(int('0b1' + bin(randbits(Characters.class_get_bit_count() - 1))[2 :], 0))
            self.characters.gen_string()
            self.seed.set(self.characters.get_string())
            self.seed_box_button2.focus_set()
        
        self.seed_box_button1 = Button(self.seed_box_frame, text="Randomise Seed", command=randomise)
        self.seed_box_button1.pack(side=LEFT)
        
        def randomise_gen() :
            a0 = self.seed.get()
            if a0 == '' :
                showerror(title, "Must first be seeded.")
                self.seed_box_entry.focus_set()
                return
            self.characters.set_string(a0)
            self.characters.gen_number()
            a0 = self.characters.get_number() * 5
            self.characters.set_number(a0 // 6)
            a0 = self.characters.get_number() * 3
            self.characters.set_number(a0 + (1 if a0 % 2 else -1))
            self.characters.gen_string()
            self.seed.set(self.characters.get_string())
            self.seed_box_button3.focus_set()
        
        self.seed_box_button2 = Button(self.seed_box_frame, text="Generate Number", command=randomise_gen)
        self.seed_box_button2.pack(side=LEFT)
        
        def lock_1(z: bool) :
            self.state_buttons_entry(self.seed_frame, DISABLED)
            if z :
                self.prime_modulus_box_entry.focus_set()
                unlock_2()
        
        def unlock_1() :
            self.state_buttons_entry(self.seed_frame, ACTIVE)
        
        def locker_1() :
            self.characters.set_string(self.seed.get())
            self.characters.gen_number()
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.seed_box_entry.focus_set()
                return
            lock_1(True)
            StringVar.set(self.prime_modulus, self.characters.get_string())
            self.collection.obj_dict_set(self.prime_modulus, self.characters.get_string())
        
        self.seed_box_button3 = Button(self.seed_box_frame0, text="Lock", command=locker_1)
        self.seed_box_button3.pack()
        
        lock_1(False)
        
        self.prime_modulus_frame = LabelFrame(self.window_frame1, text="Step 2")
        self.prime_modulus_frame.pack(side=LEFT)
        self.prime_modulus_label = Label(self.prime_modulus_frame, textvariable=self.prime_modulus_message)
        self.prime_modulus_label.pack(side=TOP)
        self.prime_modulus_box_entry = InterStringEntry(self.prime_modulus_frame, textvariable=self.prime_modulus)
        self.prime_modulus_box_entry.pack()
        
        self.prime_modulus_box_frame0 = Frame(self.prime_modulus_frame)
        self.prime_modulus_box_frame0.pack()
        
        self.prime_modulus_box_frame = Frame(self.prime_modulus_box_frame0)
        self.prime_modulus_box_frame.pack()
        
        self.lock = Lock()
        
        def prime_gen() :
            if self.lock.acquire(False) :
                Thread(target=prime_gen1, daemon=True).start()
        
        def prime_gen1() :
            aa = self.prime_modulus.get()
            if aa == '' :
                showerror(title, "The input can't be blank.")
                self.prime_modulus_box_entry.focus_set()
                self.lock.release()
                return
            self.characters.set_string(aa)
            self.characters.gen_number()
            #
            if self.characters.get_number() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.prime_modulus_box_entry.focus_set()
                self.lock.release()
                return
            #
            lock_2(False)
            self.prime_modulus_processing = True
            self.prime_modulus_message.update()
            #
            self.characters.set_number(self.characters.get_number() * 5 // 6)
            a0 = self.characters.get_number()
            self.characters.set_number(a0 + (1 if a0 % 2 else -1))
            self.characters.gen_string()
            #
            self.prime_modulus_processing = False
            self.prime_modulus_message.update()
            unlock_2()
            #
            self.prime_modulus.set(self.characters.get_string())
            self.prime_modulus_box_button2.focus_set()
            self.lock.release()
        
        self.prime_modulus_box_button1 = Button(self.prime_modulus_box_frame, text="Generate Next Prime",
                                                command=prime_gen)
        self.prime_modulus_box_button1.pack(side=LEFT)
        self.prime_modulus_box_frame.pack()
        
        def prime_modulus_test() :
            if self.lock.acquire(False) :
                Thread(target=prime_modulus_test1, daemon=True).start()
        
        def prime_modulus_test1() :
            self.characters.set_string(self.prime_modulus.get())
            self.characters.gen_number()
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.prime_modulus_box_entry.focus_set()
                self.lock.release()
                return
            #
            lock_2(False)
            self.prime_modulus_processing = True
            self.prime_modulus_try_count = 1
            self.prime_modulus_message.update()
            #
            l = local()
            #
            l.aks_or_miller = askyesnocancel(title,
                                             "Two Primality tests are provided:\n"
                                             "\t(YES) AKS          Test: end-all, be-all;\n"
                                             "\t                   explosively inefficient\n"
                                             "\t(NO ) Miller-Rabin Test: probable prime ; \n"
                                             "\t       adjustable, time-certainty trader-off\n")
            l.is_prime = False
            if l.aks_or_miller is True :
                showinfo(title, "YES")
            elif l.aks_or_miller is False :
                showinfo(title, "NO")
            else :
                showinfo(title, "NEITHER")
            # TODO WRITE!
            self.prime_modulus_processing = False
            self.prime_modulus_message.update()
            unlock_2()
            #
            if l.is_prime :
                self.prime_modulus_box_button3.focus_set()
            else :
                self.prime_modulus_box_button1.focus_set()
            self.lock.release()
        
        self.prime_modulus_box_button2 = Button(self.prime_modulus_box_frame, text="Verify Prime",
                                                command=prime_modulus_test)
        self.prime_modulus_box_button2.pack(side=LEFT)
        
        def seed_re_copy() :
            self.prime_modulus.set(self.seed.get())
            self.prime_modulus_box_entry.focus_set()
        
        self.prime_modulus_box_button3 = Button(self.prime_modulus_box_frame0, text="Re-copy", command=seed_re_copy)
        self.prime_modulus_box_button3.pack()
        
        def lock_2(z: bool) :
            self.state_buttons_entry(self.prime_modulus_frame, DISABLED)
            if z :
                self.generator_entry.focus_set()
                unlock_3()
        
        def unlock_2() :
            self.state_buttons_entry(self.prime_modulus_frame, ACTIVE)
        
        def locker_2() :
            self.characters.set_string(self.prime_modulus.get())
            self.characters.gen_number()
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.prime_modulus_box_entry.focus_set()
                return
            lock_2(True)
            StringVar.set(self.generator, self.characters.get_string())
            self.collection.obj_dict_set(self.generator, self.characters.get_string())
        
        self.prime_modulus_box_button4 = Button(self.prime_modulus_box_frame0, text="Lock", command=locker_2)
        self.prime_modulus_box_button4.pack()
        
        lock_2(False)
        
        self.generator_frame = LabelFrame(self.window_frame1, text="Step 3")
        self.generator_frame.pack(side=LEFT)
        self.generator_label = Label(self.generator_frame, textvariable=self.generator_message)
        self.generator_label.pack(side=TOP)
        self.generator_entry = InterStringEntry(self.generator_frame, textvariable=self.generator)
        self.generator_entry.pack()
        
        self.generator_box_frame0 = Frame(self.generator_frame)
        self.generator_box_frame0.pack()
        self.generator_box_frame = Frame(self.generator_box_frame0)
        self.generator_box_frame.pack()
        
        def generator_root() :
            if self.lock.acquire(False) :
                Thread(target=generator_root1, daemon=True).start()
        
        def generator_root1() :
            self.characters.set_string(self.generator.get())
            self.characters.gen_number()
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.generator_entry.focus_set()
                self.lock.release()
                return
            #
            self.generator_processing = True
            self.generator_try_count = 0
            self.generator_message.update()
            lock_3(False)
            #
            self.characters.set_number(better_isqrt(self.characters.get_number()))
            self.characters.gen_string()
            #
            self.generator_processing = False
            self.generator_message.update()
            unlock_3()
            #
            self.generator.set(self.characters.get_string())
            self.generator_box_button3.focus_set()
            self.lock.release()
        
        self.generator_box_button1 = Button(self.generator_box_frame, text="Generate Prime's Floor-Root",
                                            command=generator_root)
        self.generator_box_button1.pack(side=LEFT)
        
        def generator_re_copy() :
            self.generator.set(self.prime_modulus.get())
            self.generator_entry.focus_set()
        
        self.generator_box_button2 = Button(self.generator_box_frame, text="Re-copy", command=generator_re_copy)
        self.generator_box_button2.pack(side=LEFT)
        
        def lock_3(z: bool) :
            self.state_buttons_entry(self.generator_frame, DISABLED)
            if z :
                self.exchange_frame_reminder_button.focus_set()
                self.exchange_frame_reminder_button.configure(state=ACTIVE)
        
        def unlock_3() :
            self.state_buttons_entry(self.generator_frame, ACTIVE)
        
        def locker_3() :
            self.characters.set_string(self.prime_modulus.get())
            self.characters.gen_number()
            a0 = self.characters.get_number()
            self.characters.set_string(self.generator.get())
            self.characters.gen_number()
            a1 = self.characters.get_number() ** 2
            a2 = (self.characters.get_number() + 1) ** 2
            if not a1 <= a0 < a2 :
                showerror(title, "This primitive root is incorrect.")
                self.generator_entry.focus_set()
                return
            lock_3(True)
        
        self.generator_box_button3 = Button(self.generator_box_frame0, text="Lock", command=locker_3)
        self.generator_box_button3.pack()
        
        lock_3(False)
        
        #
        self.window_frame2 = Frame(self.window)
        self.window_frame2.grid(column=0)
        self.exchange_frame = LabelFrame(self.window_frame2, text="Step 4 - Exchange Computed Numbers")
        self.exchange_frame.pack(side=LEFT)
        self.exchange_frame_reminder_frame1 = Frame(self.exchange_frame)
        self.exchange_frame_reminder_frame1.pack()
        self.exchange_frame_reminder_label = Label(self.exchange_frame_reminder_frame1, text="Reminder, You Are: ")
        self.exchange_frame_reminder_label.pack(side=LEFT)
        
        def switcher(switch: bool) :
            if self.lock.acquire(False) :
                if switch :
                    self.exchange_frame_reminder_variable.set({"Neither" : "Alice", "Alice" : "Bob", "Bob" : "Neither"}
                                                              [self.exchange_frame_reminder_variable.get()])
                x1 = self.collection.get().get(self.exchange_frame_reminder_variable.get_name())
                if x1 == "Alice" :
                    self.state_buttons_entry(self.exchange_frame_alice_box, ACTIVE)
                    self.state_buttons_entry(self.exchange_frame_bob_box, DISABLED)
                    self.exchange_frame_alice_entry.configure(state=ACTIVE)
                    self.exchange_frame_bob_entry.configure(state=ACTIVE)
                    self.exchange_frame_locker_button.configure(state=ACTIVE)
                    self.exchange_frame_alice_entry.focus_set()
                elif x1 == "Bob" :
                    self.state_buttons_entry(self.exchange_frame_alice_box, DISABLED)
                    self.state_buttons_entry(self.exchange_frame_bob_box, ACTIVE)
                    self.exchange_frame_bob_entry.focus_set()
                else :
                    lock_4(False)
                    self.exchange_frame_alice_entry.configure(state=DISABLED)
                    self.exchange_frame_bob_entry.configure(state=DISABLED)
                    self.exchange_frame_locker_button.configure(state=DISABLED)
                    self.exchange_frame_reminder_button.focus_set()
                self.lock.release()
        
        self.exchange_frame_reminder_button = Button(self.exchange_frame_reminder_frame1,
                                                     textvariable=self.exchange_frame_reminder_variable,
                                                     command=lambda : switcher(True), state=DISABLED)
        self.exchange_frame_reminder_button.pack()
        
        self.exchange_frame_reminder_frame2 = Frame(self.exchange_frame)
        self.exchange_frame_reminder_frame2.pack()
        
        self.exchange_frame_reminder_frame2a = Frame(self.exchange_frame_reminder_frame2)
        self.exchange_frame_reminder_frame2a.pack()
        
        self.exchange_frame_alice = LabelFrame(self.exchange_frame_reminder_frame2a, text="Alice")
        self.exchange_frame_alice.pack(side=LEFT)
        self.exchange_frame_alice_label = Label(self.exchange_frame_alice, text="Calculate Number to Give Bob")
        self.exchange_frame_alice_label.pack()
        self.exchange_frame_alice_entry = InterStringEntry(self.exchange_frame_alice,
                                                           textvariable=self.exchange_frame_alice_value)
        self.exchange_frame_alice_entry.pack()
        
        self.exchange_frame_alice_value_private = 0
        self.exchange_frame_bob_value_private = 0
        
        def generate_s_random(alice_bob: bool) :
            x0 = self.exchange_frame_alice_value if alice_bob else self.exchange_frame_bob_value
            self.characters.set_string(x0.get())
            self.characters.gen_number()
            if self.characters.get_number() == 0 :
                self.characters.set_number(int(
                    '1' + ''.join('1' if randbelow(5) % 2 else '0' for _ in range(Characters.class_get_bit_count())),
                    base=2))
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                self.generator_entry.focus_set()
                return
            for y0 in scramble(Characters.class_get_bit_count() - 2) :
                if randbelow(6) % 2 :
                    self.characters.set_number(self.characters.get_number() ^ (2 ** y0))
            self.characters.gen_string()
            x0.set(self.characters.get_string())
            if alice_bob :
                self.exchange_frame_alice_value_private = self.characters.get_number()
                self.exchange_frame_alice_entry.focus_set()
            else :
                self.exchange_frame_bob_value_private = self.characters.get_number()
                self.exchange_frame_bob_entry.focus_set()
        
        def generate_public(alice_bob: bool) :
            x0 = self.exchange_frame_alice_value if alice_bob else self.exchange_frame_bob_value
            self.characters.set_string(x0.get())
            self.characters.gen_number()
            if self.characters.get_number().bit_length() < Characters.class_get_bit_count() :
                showerror(title, "Insufficient length.  It should be at least {} bits long.".format(
                    Characters.class_get_bit_count()))
                if alice_bob :
                    self.exchange_frame_alice_entry.focus_set()
                else :
                    self.exchange_frame_bob_entry.focus_set()
                return
            a0 = self.characters.get_number()  # input
            self.characters.set_string(self.prime_modulus.get())
            self.characters.gen_number()
            a1 = self.characters.get_number()  # modulus
            self.characters.set_string(self.generator.get())
            self.characters.gen_number()
            a2 = self.characters.get_number()  # generator
            #
            self.characters.set_number(pow(a2, a0, a1))
            self.characters.gen_string()
            x0.set(self.characters.get_string())
        
        self.exchange_frame_alice_box = Frame(self.exchange_frame_alice)
        self.exchange_frame_alice_box.pack()
        
        self.exchange_frame_alice_button1 = Button(self.exchange_frame_alice_box, text="Generate Private Random",
                                                   command=lambda : generate_s_random(True))
        self.exchange_frame_alice_button1.pack()
        
        self.exchange_frame_alice_button2 = Button(self.exchange_frame_alice_box, text="Generate Public",
                                                   command=lambda : generate_public(True))
        self.exchange_frame_alice_button2.pack()
        
        self.exchange_frame_bob = LabelFrame(self.exchange_frame_reminder_frame2a, text="Bob")
        self.exchange_frame_bob.pack(side=LEFT)
        self.exchange_frame_bob_label = Label(self.exchange_frame_bob, text="Calculate Number to Give Alice")
        self.exchange_frame_bob_label.pack()
        self.exchange_frame_bob_entry = InterStringEntry(self.exchange_frame_bob,
                                                         textvariable=self.exchange_frame_bob_value)
        self.exchange_frame_bob_entry.pack()
        
        self.exchange_frame_bob_box = Frame(self.exchange_frame_bob)
        self.exchange_frame_bob_box.pack()
        
        self.exchange_frame_bob_button1 = Button(self.exchange_frame_bob_box, text="Generate Private Random",
                                                 command=lambda : generate_s_random(False))
        self.exchange_frame_bob_button1.pack()
        
        self.exchange_frame_bob_button2 = Button(self.exchange_frame_bob_box, text="Generate Public",
                                                 command=lambda : generate_public(False))
        self.exchange_frame_bob_button2.pack()
        
        def lock_4(z: bool) :
            if not z :
                self.state_buttons_entry(self.exchange_frame_reminder_frame2a, DISABLED)
            else :
                self.state_buttons_entry(self.exchange_frame, DISABLED)
                self.final_frame_entry.focus_set()
                unlock_5()
        
        def unlock_4() :
            self.state_buttons_entry(self.exchange_frame_reminder_frame2a, ACTIVE)
        
        def locker_4() :
            self.characters.set_string(self.exchange_frame_alice_value.get())
            self.characters.gen_number()
            a0 = self.characters.get_number().bit_length()
            self.characters.set_string(self.exchange_frame_bob_value.get())
            self.characters.gen_number()
            a1 = self.characters.get_number().bit_length()
            self.characters.set_string(self.generator.get())
            self.characters.gen_number()
            a2 = self.characters.get_number().bit_length()
            #
            if a0 < a2 :
                showerror(title, "Alice's number must be at least {} bits long.".format(a2))
                return
            if a1 < a2 :
                showerror(title, "Bob's number must be at least {} bits long.".format(a2))
                return
            #
            lock_4(True)
        
        self.exchange_frame_reminder_frame2b = Frame(self.exchange_frame)
        self.exchange_frame_reminder_frame2b.pack()
        
        self.exchange_frame_locker_button = Button(self.exchange_frame_reminder_frame2b, text="Lock", command=locker_4)
        self.exchange_frame_locker_button.pack(side=BOTTOM)
        
        self.state_buttons_entry(self.exchange_frame, DISABLED)
        
        #
        self.window_frame3 = Frame(self.window)
        self.window_frame3.grid(column=0)
        
        self.final_frame = Labelframe(self.window_frame3, text="Step 5")
        self.final_frame.pack()
        
        self.final_frame_label1 = Label(self.final_frame, textvariable=self.final_frame_message)
        self.final_frame_label1.pack()
        
        self.final_frame_frame = Frame(self.final_frame)
        self.final_frame_frame.pack()
        self.final_frame_label2 = Label(self.final_frame_frame, text="Enter it here:")
        self.final_frame_label2.pack(side=LEFT)
        self.final_frame_entry = InterStringEntry(self.final_frame_frame, textvariable=self.final_frame_value)
        self.final_frame_entry.pack(side=LEFT)
        
        def lock_5(z: bool) :
            self.state_buttons_entry(self.final_frame, DISABLED)
            if z :
                self.final_frame_entry.focus_set()
        
        def unlock_5() :
            self.state_buttons_entry(self.final_frame, ACTIVE)
        
        def final_calculation() :
            self.characters.set_string(
                self.exchange_frame_bob_value.get() if self.exchange_frame_reminder_variable.get() == "Alice" else \
                    self.exchange_frame_alice_value.get())
            self.characters.gen_number()
            a0 = self.characters.get_number()
            #
            self.characters.set_string(self.prime_modulus.get())
            self.characters.gen_number()
            a1 = self.characters.get_number()
            #
            self.characters.set_number(pow(a0, (
                self.exchange_frame_alice_value_private if self.exchange_frame_reminder_variable.get() == "Alice" else
                self.exchange_frame_bob_value_private), a1))
            self.characters.gen_string()
            self.final_frame_value.set(self.characters.get_string())
            #
            lock_5(True)
            #
            showinfo(title, "Final key is {} bits long.".format(self.characters.get_number().bit_length()))
            self.window_up_frame_button.configure(state=ACTIVE)
        
        self.final_frame_button = Button(self.final_frame, text="Calculate joint Key, finally!",
                                         command=final_calculation)
        self.final_frame_button.pack()
        
        lock_5(False)
        
        #
        self.tutorial_frame0 = Frame(self.window_up)
        self.tutorial_frame0.grid(column=0, row=1, columnspan=2)
        self.tutorial_frame = LabelFrame(self.tutorial_frame0, text="Tutorial")
        self.tutorial_frame.pack()
        self.tutorial_button1 = Button(self.tutorial_frame, text="Khan Diffie-Hellman Full",
                                       command=lambda : open_new_tab('https://youtu.be/YEBfamv-_do'))
        self.tutorial_button1.pack(side=LEFT)
        self.tutorial_button2 = Button(self.tutorial_frame, text="Khan Diffie-Hellman Procedure",
                                       command=lambda : open_new_tab('https://youtu.be/3QnD2c4Xovk'))
        self.tutorial_button2.pack(side=LEFT)
        self.tutorial_button3 = Button(self.tutorial_frame, text="User Help", command=lambda : showinfo('Help',
                                                                                                        """
                                                                                                       """))
        self.tutorial_button3.pack(side=LEFT)
        
        #
        self.window_up_frame = Frame(self.window_manuel)
        self.window_up_frame.grid(column=0, row=3, columnspan=2, sticky=EW)
        
        self.window_up_frame_button = Button(self.window_up_frame, text="Main Page",
                                             command=lambda : self.window_main.tkraise())
        self.window_up_frame_button.grid(column=0, row=0, columnspan=2, sticky=NSEW)
        
        Grid.columnconfigure(self.window_up_frame, 0, weight=1)
        
        #
        self.window_automatic_label = Label(self.window_automatic, text=title, font=self.FONT)
        self.window_automatic_label.grid(column=0, row=0, sticky=EW)
        
        #
        self.automatic_frame = Frame(self.window_automatic)
        self.automatic_frame.grid(column=0, row=1, columnspan=2, sticky=EW)
        
        self.automatic_frame_button = Button(self.automatic_frame, text="Main Page",
                                             command=lambda : self.window_main.tkraise())
        self.automatic_frame_button.grid(column=0, row=0, columnspan=2, sticky=NSEW)
        
        Grid.columnconfigure(self.automatic_frame, 0, weight=1)
        
        #
        self.main_frame = Frame(self.window_main)
        self.main_frame.grid(column=0, row=0, sticky=NSEW)
        
        self.main_frame_label = Label(self.main_frame, text=title, font=self.FONT)
        self.main_frame_label.grid(column=0, row=0, sticky=EW)
        
        self.main_frame_button0 = Button(self.main_frame, text="Manual Process Page",
                                         command=lambda : self.window_manuel.tkraise())
        self.main_frame_button0.grid(column=0, row=1, sticky=EW)
        
        self.main_frame_button1 = Button(self.main_frame, text="Automated Process Page",
                                         command=lambda : self.window_automatic.tkraise())
        self.main_frame_button1.grid(column=0, row=2, sticky=EW)
        
        Grid.columnconfigure(self.main_frame, 0, weight=1)
        Grid.rowconfigure(self.main_frame, 0, weight=1)
        Grid.rowconfigure(self.main_frame, 1, weight=1)
        Grid.rowconfigure(self.main_frame, 2, weight=1)
        
        #
        self.exchange_frame_reminder_variable.set("Neither")
        
        # Window
        self.tk_window.wm_resizable(False, False)
        return self
    
    def run(self) :
        self.tk_window.mainloop()
        return 0


if __name__ == '__main__' :
    exit(DH().load().run())
