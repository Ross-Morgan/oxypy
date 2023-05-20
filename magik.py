from __future__ import annotations

import os
from typing import Callable, Generic, Iterator, Protocol, Type, TypeVar

__all__ = ["Default", "Option", "Panic", "Result"]

E = TypeVar("E")
T = TypeVar("T")
U = TypeVar("U")

NULL = object()

T_co = TypeVar("T_co", covariant=True)

__RAND_LEN = 64
__IS_SOME = os.urandom(__RAND_LEN).decode(errors="ignore").center(__RAND_LEN + 2)         # noqa
__INNER_SOME_VAL = os.urandom(__RAND_LEN).decode(errors="ignore").center(__RAND_LEN + 2)  # noqa

__INNER_OK_VAL = os.urandom(__RAND_LEN).decode(errors="ignore").center(__RAND_LEN + 2)    # noqa
__INNER_ERR_VAL = os.urandom(__RAND_LEN).decode(errors="ignore").center(__RAND_LEN + 2)   # noqa
__IS_OK = os.urandom(__RAND_LEN).decode(errors="ignore").center(__RAND_LEN + 2)           # noqa


class Panic(Exception):
    ...  # noqa


class Default(Protocol, Generic[T_co]):
    @classmethod
    def default(cls: Type[T_co]) -> T_co:
        ...  # noqa


class Option(Generic[T]):
    # __slots__ = [__IS_SOME, __INNER_SOME_VAL]
    def __repr__(self) -> str:
        if self.is_some():
            return f"Some({self.unwrap()})"
        return "None"

    def __setattr__(self, _name, _val):
        return NotImplemented

    # defaults

    @classmethod
    def some(cls, val: T) -> Option[T]:
        o: Option[T] = Option()

        object.__setattr__(o, __IS_SOME, True)
        object.__setattr__(o, __INNER_SOME_VAL, val)

        return o

    @classmethod
    def none(cls) -> Option[T]:
        o: Option[T] = Option()

        object.__setattr__(o, __IS_SOME, False)
        object.__setattr__(o, __INNER_SOME_VAL, NULL)

        return o

    @classmethod
    def default(cls) -> Option[T]:
        return cls.none()

    # some or none

    def is_none(self) -> bool:
        return not self.is_some()

    def is_some(self) -> bool:
        return object.__getattribute__(self, __IS_SOME)

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        if self.is_none():
            return False
        else:
            return f(self.unwrap())

    # ok

    def ok_or(self, err: E) -> Result[T, E]:
        if self.is_some():
            return Result.ok(self.unwrap())

        return Result.err(err)

    def ok_or_else(self, err: Callable[[], E]) -> Result[T, E]:
        if self.is_some():
            return Result.ok(self.unwrap())

        return Result.err(err())

    # unwrap

    def unwrap(self) -> T:
        if self.is_none():
            raise Panic("Called `Option.unwrap` on a `None` value")
        else:
            return object.__getattribute__(self, __INNER_SOME_VAL)

    def unwrap_or(self, val: T) -> T:
        if self.is_none():
            return val
        else:
            return self.unwrap()

    def unwrap_or_default(self, default: Default) -> T:
        return self.unwrap_or(default.default())

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        if self.is_none():
            return f()
        else:
            return self.unwrap()

    def expect(self, msg: str) -> T:
        if self.is_none():
            raise Panic(msg)
        else:
            return self.unwrap()

    # inspect

    def inspect(self, f: Callable[[T], U]) -> Option[T]:
        if self.is_none():
            return Option.none()

        inner_val = self.unwrap()
        f(inner_val)

        return Option.some(inner_val)

    # filter

    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        if self.is_some() and f(self.unwrap()):
            return Option.some(self.unwrap())

        return Option.none()

    # contains

    def contains(self, val: U) -> bool:
        return self.map(lambda x: x == val).unwrap_or(False)

    # and

    def and_(self, optb: Option[U]) -> Option[U]:
        if self.is_none():
            return Option.none()

        return optb

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        if self.is_none():
            return Option.none()

        return f(self.unwrap())

    # or

    def or_(self, optb: Option[T]) -> Option[T]:
        return self.map(lambda x: Option.some(x)).unwrap_or(optb)

    def or_else(self, f: Callable[[], Option[T]]):
        if self.is_some():
            return Option.some(self.unwrap())

        return f()

    # map

    def map(self, f: Callable[[T], U]) -> Option[U]:
        if self.is_none():
            return Option.none()

        modified_inner = f(self.unwrap())

        return Option.some(modified_inner)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        if self.is_none():
            return default

        return f(self.unwrap())

    def map_or_else(self, default: E) -> Result[T, E]:
        if self.is_none():
            return Result.err(default)

        return Result.ok(self.unwrap())

    # get

    def get_or_insert(self, val: T) -> T:
        if self.is_some():
            return self.unwrap()

        object.__setattr__(self, __IS_SOME, True)
        object.__setattr__(self, __INNER_SOME_VAL, val)

        return val

    def get_or_insert_default(self, default: Default) -> T:
        return self.get_or_insert(default.default())

    def get_or_insert_with(self, f: Callable[[], T]) -> T:
        return self.get_or_insert(f())

    # replace

    def replace(self, val: T) -> Option[T]:
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(self, __IS_SOME, True)
        object.__setattr__(self, __INNER_SOME_VAL, val)

        return inner

    # take

    def take(self) -> Option[T]:
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(self, __IS_SOME, False)
        object.__setattr__(self, __INNER_SOME_VAL, NULL)

        return inner

    # iter

    def iter(self) -> Iterator[T]:
        if self.is_some():
            yield self.unwrap()

        return


class Result(Generic[T, E]):
    def ok(self, val: T) -> Result[T, E]:
        return Result()

    def err(self, val: E) -> Result[T, E]:
        return Result()
