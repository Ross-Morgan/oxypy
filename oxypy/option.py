from __future__ import annotations

import os
from typing import Callable, Generic, Iterator, TypeVar

from .debug import Debug
from .default import Default
from .panic import panic
from .result import Result
from .utils import NULL

E = TypeVar("E")

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")


class Option(Debug, Default, Generic[T]):
    """
    Class containing a `Some(T)` or `None` variant

    Used where a value may not exist
    """

    vars()["__RAND_LEN"] = 64
    vars()["__IS_SOME"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )
    vars()["__INNER_SOME_VAL"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )

    def __repr__(self) -> str:
        if self.is_some():
            return f"Some({self.unwrap()!r})"
        return "None"

    def __str__(self) -> str:
        return self.__repr__()

    def __debug_str__(self) -> str:
        return self.__repr__()

    def __setattr__(self, _name, _val):
        return NotImplemented

    # defaults

    @classmethod
    def __default__(cls) -> Option[T]:
        """Specifies default variant for `Option`"""
        return cls.none()

    @classmethod
    def some(cls, val: T) -> Option[T]:
        """Creates new `Some` variant of `Option`"""
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), True)
        object.__setattr__(o, object.__getattribute__(cls, "__INNER_SOME_VAL"), val)

        return o

    @classmethod
    def none(cls) -> Option[T]:
        """Creates new `None` variant of `Option`"""
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), False)
        object.__setattr__(o, object.__getattribute__(cls, "__INNER_SOME_VAL"), NULL)

        return o

    # some or none

    def is_none(self) -> bool:
        """
        If self is `Some` variant, returns `False`

        If self is `None` variant, returns `True`
        """
        return not self.is_some()

    def is_some(self) -> bool:
        """
        If self is `Some` variant, returns `True`

        If self is `None` variant, returns `False`
        """
        return object.__getattribute__(self, object.__getattribute__(self, "__IS_SOME"))

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        If self is `Some` variant and matches predicate, returns `True`

        If self is `None` variant, returns `False`
        """
        if self.is_none():
            return False
        else:
            return f(self.unwrap())

    # ok

    def ok_or(self, err: E) -> Result[T, E]:
        """
        If self is `Some` variant, returns contained value wrapped in `Ok`

        If self is `None` variant, returns specified value wrapped in `Err`
        """
        if self.is_some():
            return Result.ok(self.unwrap())

        return Result.err(err)

    def ok_or_else(self, err: Callable[[], E]) -> Result[T, E]:
        """
        If self is `Some` variant, returns contained value wrapped in `Ok`

        If self is `None` variant, returns result of specified predicate
        wrapped in `Err`
        """
        if self.is_some():
            return Result.ok(self.unwrap())

        return Result.err(err())

    # unwrap

    def unwrap(self) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, panics
        """
        if self.is_none():
            panic("Called `Option.unwrap` on a `None` value")
        else:
            return object.__getattribute__(
                self, object.__getattribute__(self, "__INNER_SOME_VAL")
            )

    def unwrap_or(self, val: T) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, returns specified value
        """
        if self.is_none():
            return val
        else:
            return self.unwrap()

    def unwrap_or_default(self, default: Default[T]) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, returns default value for type
        """
        return self.unwrap_or(default.__default__())

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, returns result of specified predicate
        """
        if self.is_none():
            return f()
        else:
            return self.unwrap()

    def expect(self, msg: str) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, panics with specified error message
        """
        if self.is_none():
            panic(msg)
        else:
            return self.unwrap()

    # inspect

    def inspect(self, f: Callable[[T], U]) -> Option[T]:
        """Calls predicate on `Some` variant without modifying it"""
        if self.is_none():
            return Option.none()

        inner_val = self.unwrap()
        f(inner_val)

        return Option.some(inner_val)

    # filter

    def filter(self, f: Callable[[T], bool]) -> Option[T]:
        """
        If self is `Some` variant, returns `Some` variant if contained value matches predicate

        If self is `None` variant, returns `None` variant
        """
        if self.is_some() and f(self.unwrap()):
            return Option.some(self.unwrap())

        return Option.none()

    # contains

    def contains(self, val: U) -> bool:
        """
        If self is `Some` variant, and contained value
        equals specified value, returns `True`

        If self is `None` variant, returns `False`
        """
        return self.map(lambda x: x == val).unwrap_or(False)

    # and

    def and_(self, optb: Option[U]) -> Option[U]:
        """
        If self is `Some` variant, returns specified option

        If self is `None` variant, returns `None` variant
        """
        if self.is_none():
            return Option.none()

        return optb

    def and_then(self, f: Callable[[T], Option[U]]) -> Option[U]:
        """
        If self is `Some` variant, returns result of specified predicate

        If self is `None` variant, returns `None` variant
        """
        if self.is_none():
            return Option.none()

        return f(self.unwrap())

    # or

    def or_(self, optb: Option[T]) -> Option[T]:
        """
        If self is `Some` variant, returns contained value wrapped in `Some`

        If self is `None` variant, returns specified option
        """
        return self.map(lambda x: Option.some(x)).unwrap_or(optb)

    def or_else(self, f: Callable[[], Option[T]]):
        """
        If self is `Some` variant, returns contained value wrapped in `Some`

        If self is `None` variant, returns result of specified predicate
        """
        if self.is_some():
            return Option.some(self.unwrap())

        return f()

    # map

    def map(self, f: Callable[[T], U]) -> Option[U]:
        """
        If self is `Some` variant, returns `Some` variant with modified inner value

        If self is `None` variant, returns `None` variant
        """
        if self.is_none():
            return Option.none()

        modified_inner = f(self.unwrap())

        return Option.some(modified_inner)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        If self is `Some` variant, returns `Some` variant with modified inner value

        If self is `None` variant, returns `None` variant
        """
        if self.is_none():
            return default

        return f(self.unwrap())

    def map_or_else(self, default: Callable[[], U], f: Callable[[T], U]) -> U:
        """
        If self is `Some` variant, returns modified inner value

        If self is `None` variant, returns result of specified predicate
        """
        if self.is_none():
            return default()

        return f(self.unwrap())

    # get

    def get_or_insert(self, val: T) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, sets to and returns specified value
        """
        if self.is_some():
            return self.unwrap()

        object.__setattr__(self, object.__getattribute__(self, "__IS_SOME"), True)
        object.__setattr__(self, object.__getattribute__(self, "__INNER_SOME_VAL"), val)

        return val

    def get_or_insert_default(self, default: Default) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, sets to and returns default for type
        """
        return self.get_or_insert(default.__default__())

    def get_or_insert_with(self, f: Callable[[], T]) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, sets to and returns predicate result
        """
        return self.get_or_insert(f())

    # replace

    def replace(self, val: T) -> Option[T]:
        """Returns contained value then sets inner value to specified value"""
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(self, object.__getattribute__(self, "__IS_SOME"), True)
        object.__setattr__(self, object.__getattribute__(self, "__INNER_SOME_VAL"), val)

        return inner

    # take

    def take(self) -> Option[T]:
        """Returns copy of self, and makes self `None`"""
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(self, object.__getattribute__(self, "__IS_SOME"), False)
        object.__setattr__(
            self, object.__getattribute__(self, "__INNER_SOME_VAL"), NULL
        )

        return inner

    # iter

    def iter(self) -> Iterator[T]:
        """Transforms self into an iterator containing the `Some` variant"""
        if self.is_some():
            yield self.unwrap()

        return

    # zip

    def zip_(self, other: Option[U]) -> Option[tuple[T, U]]:
        """Zips `self` with `other`"""
        if not (self.is_some() and other.is_some()):
            return Option.none()

        return Option.some(
            (
                self.unwrap(),
                other.unwrap(),
            )
        )

    def zip_with(self, other: Option[U], f: Callable[[T, U], R]) -> Option[R]:
        """Zips `self` and `other` with the specified predicate"""
        if not (self.is_some() and other.is_some()):
            return Option.none()

        return Option.some(f(self.unwrap(), other.unwrap()))
