#!/usr/bin/python3
from collections import deque, namedtuple
from functools import reduce
from math import prod
from typing import *

"""
Op: + - * / % ** < > <=,≤ >=,≥ <> == !=,≠ !!,¬ &&,∧ ||,∨ << >> ~ & ^,⊕ | =,≔ ?,tn λ (λ)
Source: https://pastebin.com/v2EkGWvr
Normally, a language takes in text (source) and lexes it into bytecode.  That bytecode is then enacted by interpreting, transpiling, or compiling it.
This module is intended for describing and executing calculations.  It's given a sort-of bytecode and it gives back a source text and the calculations' result.
"""

T_NUM_TYPE = Union[int, float]
T_OP_TYPE = Union[T_NUM_TYPE, 'Op']
T_OPERANDS_EVAL = Tuple[T_NUM_TYPE, ...]
T_OPERANDS_NOT_EVAL = Tuple[T_OP_TYPE, ...]
T_OP_FXN = Union[Callable[[T_OPERANDS_EVAL], T_OP_TYPE], Callable[[T_OPERANDS_NOT_EVAL, bool], T_OP_TYPE]]

_T1 = TypeVar('T1')


def neighbors(x: Iterable[_T1]) -> Iterable[Tuple[_T1, _T1]]:
    try:
        last = next(ix := iter(x))
    except StopIteration:
        return
    for c in ix:
        yield last, c
        last = c


def flat(elements: Iterable[Iterable[_T1]]) -> Iterable[_T1]:
    for e in elements:
        yield from e


op_names: List[Tuple[str, Type['Op']]] = []


def base_f(v: T_OPERANDS_EVAL) -> 'Op':
    return num(v[0])


class Op:
    _operands: T_OPERANDS_NOT_EVAL
    _value: Optional[T_OP_TYPE]
    _evaluated: bool = False
    _fxn: T_OP_FXN = base_f
    _fxn_name: str = 'f'
    _repr_fxn: bool = False
    _pre_eval_param: bool = True
    _c_name: str = 'Op'

    def __init__(self, *operands: T_OP_TYPE, fxn: T_OP_FXN = ..., fxn_name: str = ..., repr_fxn: bool = ..., pep: bool = ...):
        self._operands = operands
        self._value = None
        if fxn is not Ellipsis:
            self._fxn = fxn
        if fxn_name is not Ellipsis:
            self._fxn_name = fxn_name
        if repr_fxn is not Ellipsis:
            self._repr_fxn = repr_fxn
        elif self._c_name == 'Op':
            self._repr_fxn = True
        if pep is not Ellipsis:
            self._pre_eval_param = pep

    def evaluate(self, redo: bool = False) -> T_OP_TYPE:
        if not self._evaluated or redo:
            fxn, operands = self._fxn, self._operands
            self._value = (fxn(evaluate_operands(operands, redo, True)) if self._pre_eval_param else fxn(operands, redo))
            self._evaluated = True
        return self._value

    def to_num(self, redo: bool = False) -> T_NUM_TYPE:
        return self.evaluate(redo).to_num(redo)

    def to_var(self, redo: bool = False) -> Optional['Variable']:  # Use with caution:  the variable returned might not mirror self.evaluate()
        return self.evaluate(redo).to_var(redo)

    def _s_ops(self) -> Iterable[str]:
        return (x.__str__() for x in self._operands)

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, *self._s_ops())))

    @property
    def source(self) -> str:
        return self.__str__()

    def _r_ops(self) -> Iterable[str]:
        return (x.__repr__() for x in self._operands)

    def __repr__(self) -> str:
        params = deque(map(repr, self._operands))
        op = self.__class__  # works for derivative classes

        def new(attr_name: str, p_name: str):
            if getattr(op, attr_name) != (p_value := getattr(self, attr_name)):
                params.append(f'{p_name} = {repr(p_value)}')

        if self._repr_fxn:
            new('_fxn', 'fxn')
            new('_fxn_name', 'fxn_name')
        new('_repr_fxn', 'repr_fxn')
        new('_pre_eval_param', 'pep')
        return '{}({})'.format(self._c_name, ', '.join(params))

    @property
    def py_source(self) -> str:
        return self.__repr__()

    @property
    def evaluated(self):
        return self._evaluated

    @property
    def value(self) -> Optional[T_OP_TYPE]:
        return self._value

    @property
    def fxn(self) -> T_OP_FXN:
        return self._fxn

    @property
    def c_name(self) -> str:
        return self._c_name

    @classmethod
    def add_to_names(cls):
        op_names.append((cls._c_name, cls))


Op.add_to_names()


def evaluate_operands(operands: Iterable[Op], redo: bool, make_tuple: bool) -> Union[Tuple[T_NUM_TYPE, ...], Iterable[T_NUM_TYPE]]:
    g = (x.to_num(redo) for x in operands)
    return tuple(g) if make_tuple else g


class Base(Op):  # no-op/number
    _evaluated = True
    _c_name = 'num'

    def __init__(self, value: T_NUM_TYPE):
        Op.__init__(self)
        self._value = value

    def evaluate(self, _ = ...) -> T_NUM_TYPE:
        return self._value

    def to_num(self, _ = ...) -> T_NUM_TYPE:
        return self._value

    def to_var(self, _: bool = ...) -> Optional['Variable']:
        return None

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return '{}({})'.format(self._c_name, repr(self._value))


def number_else0(x: Op = ...) -> Op:
    return num(0) if x is Ellipsis else x


NoOp = num = Base
num.add_to_names()


class DOp(Op):
    def __init__(self, *operands: Op):
        Op.__init__(self, *operands)


def add_f(v: T_OPERANDS_EVAL) -> Op:
    return num(sum(v))


class Add(DOp):
    _fxn = add_f
    _fxn_name = '+'
    _c_name = 'add'


add = Add
add.add_to_names()


def sub_f(v: T_OPERANDS_EVAL) -> Op:
    return num(next((vs := iter(v)), 0) - sum(vs))


class Sub(DOp):
    _fxn = sub_f
    _fxn_name = '-'
    _c_name = 'sub'


sub = Sub
sub.add_to_names()


def neg_f(v: T_OPERANDS_EVAL) -> Op:
    return num(-(v[0]))


class Neg(DOp):
    _fxn = neg_f
    _fxn_name = '-'
    _c_name = 'neg'

    def __str__(self) -> str:
        return '-' + str(self._operands[0])


neg = Neg
neg.add_to_names()


def mul_f(v: T_OPERANDS_EVAL) -> Op:
    return num(prod(v))


class Mul(DOp):
    _fxn = mul_f
    _fxn_name = '*'
    _c_name = 'mul'


mul = Mul
mul.add_to_names()


def div0_safe(fxn: T_OP_FXN) -> T_OP_FXN:
    def safe_fxn(v: T_OPERANDS_EVAL) -> Op:
        try:
            return fxn(v)
        except ZeroDivisionError:
            return num(0.00)  # TheC language returns 0.0f for 0.0f / 0.0f.

    return safe_fxn


@div0_safe
def div_f(v: T_OPERANDS_EVAL) -> Op:
    return num(next(vs := iter(v), 0) / prod(vs))


class Div(DOp):
    _fxn = div_f
    _fxn_name = '/'
    _c_name = 'div'


div = Div
div.add_to_names()


def fdiv2(a, b):
    return a // b


@div0_safe
def fdiv_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(fdiv2, v))


class Fdiv(DOp):
    _fxn = fdiv_f
    _fxn_name = '//'
    _c_name = 'fdiv'


fdiv = Fdiv
fdiv.add_to_names()


def mod2(a, b):
    return a % b


@div0_safe
def mod_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(mod2, v))


class Mod(DOp):
    _fxn = mod_f
    _fxn_name = '%'
    _c_name = 'mod'


mod = Mod
mod.add_to_names()


def pow2(a, b):
    return a ** b


@div0_safe
def power_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(pow2, v))  # left to right, yes.


class Pow(DOp):
    _fxn = power_f
    _fxn_name = '**'
    _c_name = 'xpow'


xpow = Pow
xpow.add_to_names()


@div0_safe
def bpm_f(v: T_OPERANDS_EVAL) -> Op:
    return num(pow(v[0], v[1], v[2]))


class BPM(Op):
    _fxn = bpm_f
    _fxn_name = '**%'
    _c_name = 'bpm'

    def __init__(self, base: Op, power: Op, modulus: Op):
        Op.__init__(self, base, power, modulus)


bpm = BPM
bpm.add_to_names()


def les_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a < b for (a, b) in neighbors(v)))


class Les(DOp):
    _fxn = les_f
    _fxn_name = '<'
    _c_name = 'les'


les = Les
les.add_to_names()


def gtr_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a > b for (a, b) in neighbors(v)))


class Gtr(DOp):
    _fxn = gtr_f
    _fxn_name = '>'
    _c_name = 'gtr'


gtr = Gtr
gtr.add_to_names()


def leq_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a <= b for (a, b) in neighbors(v)))


class Leq(DOp):
    _fxn = leq_f
    _fxn_name = '<='
    _c_name = 'leq'


leq = Leq
leq.add_to_names()


def geq_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a >= b for (a, b) in neighbors(v)))


class Geq(DOp):
    _fxn = geq_f
    _fxn_name = '>='
    _c_name = 'geq'


geq = Geq
geq.add_to_names()


def cmp2(a, b) -> int:
    return 0 if a < b else (1 if a == b else 2)


def cmp_f(v: T_OPERANDS_EVAL) -> Op:
    r = set(cmp2(a, b) for (a, b) in neighbors(v))
    return num(r.pop() if len(r) == 1 else 3)


class Cmp(DOp):
    _fxn = cmp_f
    _fxn_name = '<>'
    _c_name = 'cmp'


cmp = Cmp
cmp.add_to_names()


def equ_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a == b for (a, b) in neighbors(v)))


class Equ(DOp):
    _fxn = equ_f
    _fxn_name = '=='
    _c_name = 'equ'


equ = Equ
equ.add_to_names()


def neq_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * all(a != b for (a, b) in neighbors(v)))


class Neq(DOp):
    _fxn = neq_f
    _fxn_name = '!='
    _c_name = 'neq'


neq = Neq
neq.add_to_names()


def xnot_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * (not v[0]))


class Xnot(DOp):
    _fxn = xnot_f
    _fxn_name = '!'
    _c_name = 'xnot'

    def __str__(self) -> str:
        return self._fxn_name + str(self._operands[0])


xnot = Xnot
xnot.add_to_names()


def xand_f(v: T_OPERANDS_EVAL) -> Op:  # unit product
    return num(1 * all(v))


class Xand(DOp):
    _fxn = xand_f
    _fxn_name = '&&'
    _c_name = 'xand'


xand = Xand
xand.add_to_names()


def yor_f(v: T_OPERANDS_EVAL) -> Op:
    return num(1 * any(v))


class Yor(DOp):
    _fxn = yor_f
    _fxn_name = '||'
    _c_name = 'yor'


yor = Yor
yor.add_to_names()


def shift_left_f(v: T_OPERANDS_EVAL) -> Op:
    return num(next((vs := iter(v)), 0) << sum(vs))


class ShiftLeft(DOp):
    _fxn = shift_left_f
    _fxn_name = '<<'
    _c_name = 'shift_left'


shift_left = ShiftLeft
shift_left.add_to_names()


def shift_right_f(v: T_OPERANDS_EVAL) -> Op:
    return num(next((vs := iter(v)), 0) >> sum(vs))


class ShiftRight(DOp):
    _fxn = shift_right_f
    _fxn_name = '>>'
    _c_name = 'shift_right'


shift_right = ShiftRight
shift_right.add_to_names()


def bnot_f(v: T_OPERANDS_EVAL) -> Op:
    return num(~(v[0]))


class Bnot(DOp):
    _fxn = bnot_f
    _fxn_name = '~'
    _c_name = 'bnot'


bnot = Bnot
bnot.add_to_names()


def band2(a, b):
    return a & b


def band_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(band2, v))


class Band(DOp):
    _fxn = band_f
    _fxn_name = '&'
    _c_name = 'band'


band = Band
band.add_to_names()


def xor2(a, b):
    return a ^ b


def xor_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(xor2, v))


class Xor(DOp):
    _fxn = xor_f
    _fxn_name = '^'
    _c_name = 'xor'


xor = Xor
xor.add_to_names()


def bor2(a, b):
    return a | b


def bor_f(v: T_OPERANDS_EVAL) -> Op:
    return num(reduce(bor2, v))


class Bor(DOp):
    _fxn = bor_f
    _fxn_name = '|'
    _c_name = 'bor'


bor = Bor
bor.add_to_names()


def show_f(v: T_OPERANDS_EVAL) -> Op:
    return num(v[0])


class Show(DOp):
    _fxn = show_f
    _fxn_name = '='
    _c_name = 'show'

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, *('[{} {}]'.format(str(operand), operand.to_num()) for operand in self._operands))))


show = Show
show.add_to_names()


class Namespace:
    _SYMBOL_STACK: Deque[Dict[str, Op]] = deque()
    _names: Dict[str, Op]

    def __init__(self):
        self._names = {}

    def __del__(self):
        self._names.clear()  # Protect variables.

    def __enter__(self):  # Please don't enter the same ns twice.
        self._SYMBOL_STACK.append(self._names)

    def __exit__(self, *_):
        self._SYMBOL_STACK.pop()

    def set(self, name: str, value: Op):
        self._names[name] = value

    def get(self, name: str, default: Op = ...) -> Op:
        for nss in reversed(self._SYMBOL_STACK):
            try:
                return nss[name]
            except KeyError:
                pass
        return number_else0(default)

    def has(self, name: str) -> bool:
        return any(name in nss for nss in reversed(self._SYMBOL_STACK))


def new_ns() -> Namespace:
    return Namespace()


gns = new_ns()  # general namespace


class Variable(Op):
    _c_name = 'var'
    _name: str

    def __init__(self, name: str):
        Op.__init__(self, self)
        self._name = name

    def evaluate(self, redo: bool = False) -> T_OP_TYPE:
        if not self._evaluated or redo:
            self._value = self.get()
            self._evaluated = True
        return self._value

    def to_var(self, _: bool = ...) -> Optional['Variable']:
        return self

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return "{}({})".format(self._c_name, repr(self._name))

    @property
    def v_name(self) -> str:
        return self._name

    def get(self, default: Op = ...) -> Op:
        return gns.get(self._name, default)

    def set(self, x: Op):
        gns.set(self._name, x)


var = Variable
var.add_to_names()

T_SET_PAIR = Tuple[Variable, Op]
TT_SET_PAIR = Tuple[T_SET_PAIR, ...]


def xset_f(v: TT_SET_PAIR, redo: bool) -> Op:
    for v_named, new_value in v:
        v_named.to_var(redo).set(num(new_value.to_num(redo)))
    return num(v[0][1].to_num())  # already (re)calculated


class Xset(Op):
    _operands: TT_SET_PAIR
    _fxn_name = ':='
    _pre_eval_param = False
    _c_name = 'xset'

    def __init__(self, *operands: T_SET_PAIR):
        Op.__init__(self, *operands)

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, *(f'[{str(n)} {str(v)}]' for (n, v) in self._operands))))

    def __repr__(self) -> str:
        return '{}({})'.format(self._c_name, ', '.join((f'({repr(n)}, {repr(v)})' for (n, v) in self._operands)))


xset = Xset
xset.add_to_names()

T_TN_OPERAND = Tuple[Op, Op]
TT_TN_OPERAND = Tuple[TT_SET_PAIR, ...]

tnf_type = namedtuple('tnf_type', ('case', 'r_value'))


def tn_f(sw: Op, v: TT_TN_OPERAND, default: Op, redo: bool) -> Op:
    switch = sw.to_num(redo)
    for x in v:
        clause = tnf_type(*x)
        if switch == clause.case.to_num(redo):
            return num(clause.r_value.to_num(redo))
    return num(default.to_num(redo))


class Tn(Op):
    _operands: TT_TN_OPERAND
    _fxn_name = '?'
    _pre_eval_param = False
    _c_name = 'tn'
    _switch: Op
    _default: Op

    def __init__(self, value: Op, *operands: T_TN_OPERAND, otherwise: Op = ...):
        Op.__init__(self, *operands)
        self._switch = value
        self._default = number_else0(otherwise)

    def evaluate(self, redo: bool = False) -> T_OP_TYPE:
        if not self._evaluated or redo:
            self._value = tn_f(self._switch, self._operands, self._default, redo)
            self._evaluated = True
        return self._value

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, str(self._switch), *(f'[{str(n)} {str(v)}]' for (n, v) in self._operands), f'[{str(self._default)}]')))

    def __repr__(self) -> str:
        return '{}({})'.format(self._c_name, ', '.join((repr(self._switch), *(f'({repr(n)}, {repr(v)})' for (n, v) in self._operands), *((f'otherwise = {repr(df)}',) if (df := self._default).to_num() != 0 else ()))))


tn = Tn
tn.add_to_names()


class Lambda(Op):
    _operands: Tuple[Variable, ...]
    _fxn_name = 'λ'
    _c_name = 'lam'
    _var: Variable
    _expr: Op

    def __init__(self, name: str, *parameters: Variable, expression: Op):
        Op.__init__(self, *parameters)
        self._var = Variable(name)
        self._expr = expression

    def evaluate(self, redo: bool = False) -> T_OP_TYPE:
        if not self._evaluated or redo:
            self._var.set(self)
            self._value = self
            self._evaluated = True
        return self._value

    def to_num(self, redo: bool = False) -> T_NUM_TYPE:
        return Call(self).to_num(redo)

    def to_var(self, _: bool = ...) -> Optional['Variable']:
        return self._var

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, self.v_name, '({})'.format(' '.join(p.v_name for p in self._operands)), str(self._expr))))

    def __repr__(self) -> str:
        return '{}({})'.format(self._c_name, ', '.join((repr(self.v_name), *((repr(p.v_name) for p in self._operands)), f'expression = {repr(self._expr)}')))

    @property
    def v_name(self):
        return self._var.v_name

    def invoke(self) -> Op:
        return self._expr.evaluate(True)  # return value may be variable.


lam = Lambda
lam.add_to_names()


class Call(Op):
    _fxn_name = '(λ{})'
    _c_name = 'call'
    _l_fxn: Lambda

    def __init__(self, fxn: Lambda, *operands: Op):
        Op.__init__(self, *operands, fxn_name = Call._fxn_name.format(fxn.v_name))
        self._l_fxn = fxn

    def evaluate(self, redo: bool = False) -> T_OP_TYPE:
        if not self._evaluated or redo:
            with new_ns():
                fxn = self._l_fxn
                n: Variable
                # noinspection PyProtectedMember
                for n, v in zip(fxn._operands, self._operands):
                    n.to_var(redo).set(v.evaluate(redo))  # lazy
                self._value = fxn.invoke()
            self._evaluated = True
        return self._value

    def to_var(self, _: bool = ...) -> Optional['Variable']:
        return None

    def __str__(self) -> str:
        return '({})'.format(' '.join((self._fxn_name, '({})'.format(' '.join(self._s_ops())))))

    def __repr__(self) -> str:
        return '{}({})'.format(self._c_name, ', '.join((repr(self.v_name), '({})'.format(', '.join(self._r_ops())),)))

    @property
    def v_name(self):
        return self._l_fxn.v_name


call = Call
call.add_to_names()

op_names: Tuple[Tuple[str, Type['Op']], ...] = tuple(op_names)
