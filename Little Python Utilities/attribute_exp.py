#!/usr/bin/python3
from typing import Callable, Dict, Optional, Tuple, TypeVar


# noinspection PyTypeHints
_T1 = TypeVar('ObjectType')
# noinspection PyTypeHints
_T2 = TypeVar('AttributeType')
# common
_OT2 = Optional[_T2]


class AttributeLocker:  # https://pastebin.com/q88V9zav
    _object: _T1
    _attr_name: str
    _original: _OT2

    def __init__(self, obj: _T1, name: str):
        self._object = obj
        self._attr_name = name
        self._original = None

    def get(self) -> _T2:
        return getattr(self._object, self._attr_name)

    def set(self, new: _T2):
        setattr(self._object, self._attr_name, new)

    def apply(self, fxn: Callable[[_T2], _T2]) -> _T2:
        obj, name = self._object, self._attr_name
        setattr(obj, name, (new := fxn(getattr(obj, name))))
        return new

    def __enter__(self):
        self._original = self.get()

    def __exit__(self, *_):
        self.set(self._original)
        self._original = None

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def original(self) -> _T2:
        return self._original


class AttributesLocker:
    _object: _T1
    _names: Tuple[str, ...]
    _originals: Dict[str, _OT2]

    def __init__(self, obj: _T1, *names: str):
        self._object = obj
        self._names = names
        self._originals = {}

    def set(self, attr: str, value: _T2):
        setattr(self._object, attr, value)

    def get(self, attr: str) -> _OT2:
        return getattr(self._object, attr, None)

    def apply(self, attr: str, fxn: Callable[[_T2], _T2]) -> _T2:
        setattr((obj := self._object), attr, (new := fxn(getattr(obj, attr))))
        return new

    def __enter__(self):
        obj = self._object
        self._originals.update({n: getattr(obj, n) for n in self._names})

    def __exit__(self, *_):
        obj = self._object
        orig = self._originals
        for nv in orig.items():
            setattr(obj, *nv)
        orig.clear()

    @property
    def names(self) -> Tuple[str, ...]:
        return self._names

    def name(self, index: int) -> str:
        return self._names[index]

    def original(self, attr: str, default: _OT2 = None) -> _OT2:
        return self._originals.get(attr, default)
