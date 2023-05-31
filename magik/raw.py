from __future__ import annotations

import os
from typing import Callable, Generic, Iterator, TypeVar

from .utils import NULL, Default, Panic

__all__ = ["Option"]

E = TypeVar("E")
F = TypeVar("F")

T = TypeVar("T")
U = TypeVar("U")

T_co = TypeVar("T_co", covariant=True)


class Option(Generic[T]):
    vars()["__RAND_LEN"] = 64
    vars()["__IS_SOME"] = os.urandom(vars()["__RAND_LEN"]).decode(errors="ignore").center(vars()["__RAND_LEN"] + 2)         # noqa
    vars()["__INNER_SOME_VAL"] = os.urandom(vars()["__RAND_LEN"]).decode(errors="ignore").center(vars()["__RAND_LEN"] + 2)  # noqa

    def __repr__(self) -> str:
        if self.is_some():
            return f"Some({self.unwrap()})"
        return "None"

    def __setattr__(self, _name, _val):
        return NotImplemented

    # defaults

    @classmethod
    def some(cls, val: T) -> Option[T]:
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), True)
        object.__setattr__(o, object.__getattribute__(cls, "__INNER_SOME_VAL"), val)

        return o

    @classmethod
    def none(cls) -> Option[T]:
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), False)
        object.__setattr__(o, object.__getattribute__(cls, "__INNER_SOME_VAL"), NULL)

        return o

    @classmethod
    def default(cls) -> Option[T]:
        return cls.none()

    # some or none

    def is_none(self) -> bool:
        return not self.is_some()

    def is_some(self) -> bool:
        return not not object.__getattribute__(self, object.__getattribute__(self, "__INNER_SOME_VAL"))

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
            return object.__getattribute__(self, object.__getattribute__(self, "__INNER_SOME_VAL"))

    def unwrap_or(self, val: T) -> T:
        if self.is_none():
            return val
        else:
            return self.unwrap()

    def unwrap_or_default(self, default: Default[T]) -> T:
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

        object.__setattr__(self, object.__setattr__(self, "__IS_SOME"), True)
        object.__setattr__(self, object.__setattr__(self, "__INNER_SOME_VAL"), val)

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

        object.__setattr__(self, object.__getattribute__(self, "__IS_SOME"), True)
        object.__setattr__(self, object.__getattribute__(self, "__INNER_SOME_VAL"), val)

        return inner

    # take

    def take(self) -> Option[T]:
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(self, object.__getattribute__(self, "__IS_SOME"), False)
        object.__setattr__(self, object.__getattribute__(self, "__INNER_SOME_VAL"), NULL)

        return inner

    # iter

    def iter(self) -> Iterator[T]:
        if self.is_some():
            yield self.unwrap()

        return


class Result(Generic[T, E]):
    vars()["__RAND_LEN"] = 64
    vars()["__INNER_OK_VAL"] = os.urandom(vars()["__RAND_LEN"]).decode(errors="ignore").center(vars()["__RAND_LEN"] + 2)    # noqa
    vars()["__INNER_ERR_VAL"] = os.urandom(vars()["__RAND_LEN"]).decode(errors="ignore").center(vars()["__RAND_LEN"] + 2)   # noqa
    vars()["__IS_OK"] = os.urandom(vars()["__RAND_LEN"]).decode(errors="ignore").center(vars()["__RAND_LEN"] + 2)           # noqa

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Ok({self.unwrap()})"
        else:
            return f"Err({self.unwrap_err()})"

    def __str__(self) -> str:
        return self.__repr__()

    def __setattr__(self, _name, _value) -> None:
        return NotImplemented

    # defaults

    @classmethod
    def ok(cls, val: T) -> Result[T, E]:
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), True)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_OK_VAL"), val)    # noqa
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_ERR_VAL"), NULL)  # noqa

        return r

    @classmethod
    def err(cls, val: E) -> Result[T, E]:
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), False)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_OK_VAL"), NULL)  # noqa
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_ERR_VAL"), val)  # noqa

        return r

    # ok or err

    def is_ok(self) -> bool:
        return not not object.__getattribute__(self, object.__getattribute__(self, "__IS_OK"))

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        if self.is_err():
            return False

        return f(self.unwrap())

    def is_err(self) -> bool:
        return not object.__getattribute__(self, object.__getattribute__(self, "__IS_OK"))

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        if self.is_ok():
            return False

        return f(self.unwrap_err())

    def into_ok(self) -> Option[T]:
        if self.is_ok():
            return Option.some(self.unwrap())
        else:
            return Option.none()

    def into_err(self) -> Option[E]:
        if self.is_err():
            return Option.some(self.unwrap_err())
        else:
            return Option.none()

    # unwrap

    def unwrap(self) -> T:
        if self.is_err():
            raise Panic("Called `Result.unwrap` on an `Err` variant")
        else:
            return object.__getattribute__(self, object.__getattribute__(self, "__INNER_OK_VAL"))

    def unwrap_or(self, val: E) -> T:
        if self.is_err():
            return val
        else:
            return self.unwrap()

    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        if self.is_err():
            return f(self.unwrap_err())
        else:
            return self.unwrap()

    def unwrap_or_default(self, default: Default[T]) -> T:
        if self.is_err():
            return default.default()
        else:
            return self.unwrap()

    def unwrap_err(self) -> E:
        if self.is_ok():
            raise Panic("Called `Result.unwrap_err` on an `Ok` variant")
        else:
            return object.__getattribute__(self, object.__getattribute__(self, "__INNER_ERR_VAL"))

    def expect(self, msg: str) -> T:
        if self.is_err():
            raise Panic(msg)
        else:
            return self.unwrap()

    def expect_err(self, msg: str) -> E:
        if self.is_ok():
            raise Panic(msg)
        else:
            return self.unwrap_err()

    # contains

    def contains(self, val: U) -> bool:
        if self.is_ok():
            return self.unwrap() == val
        else:
            return False

    def contains_err(self, val: F) -> bool:
        if self.is_err():
            return self.unwrap_err() == val
        else:
            return False

    # map

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        if self.is_ok():
            return Result.ok(f(self.unwrap()))
        else:
            return Result.err(self.unwrap_err())

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default()

    def map_err(self, f: Callable[[E], F]) -> Result[T, F]:
        if self.is_ok():
            return Result.ok(self.unwrap())
        else:
            return Result.err(f(self.unwrap_err()))

    # inspect

    def inspect(self, f: Callable[[T], None]) -> Result[T, E]:
        if self.is_ok():
            f(self.unwrap())

            return Result.ok(self.unwrap())
        else:
            return Result.err(self.unwrap_err())

    def inspect_err(self, f: Callable[[E], None]) -> Result[T, E]:
        if self.is_ok():
            return Result.ok(self.unwrap())
        else:
            f(self.unwrap_err())

            return Result.err(self.unwrap_err())

    # iter

    def iter(self) -> Iterator[T]:
        if self.is_ok():
            yield self.unwrap()

        return

    def iter_err(self) -> Iterator[E]:
        if self.is_err():
            yield self.unwrap_err()

        return
