from __future__ import annotations

import os
from typing import Callable, Generic, Iterator, TypeVar

from .debug import Debug
from .default import Default
from .panic import panic
from .utils import NULL

__all__ = ["Result"]

E = TypeVar("E")
F = TypeVar("F")

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")


class Result(Debug, Generic[T, E]):
    """
    Class containing either an `Ok(T)` or `Err(E)` variant

    Used for expressing where a process may be erraneous or may fail
    """

    vars()["__RAND_LEN"] = 64
    vars()["__INNER_OK_VAL"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )
    vars()["__INNER_ERR_VAL"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )
    vars()["__IS_OK"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )

    def __repr__(self) -> str:
        if self.is_ok():
            return f"Ok({self.unwrap()!r})"
        else:
            return f"Err({self.unwrap_err()!r})"

    def __str__(self) -> str:
        return self.__repr__()

    def __debug_str__(self) -> str:
        return self.__repr__()

    def __setattr__(self, _name, _value) -> None:
        pass

    # defaults

    @classmethod
    def ok(cls, val: T) -> Result[T, E]:
        """Creates a new `Ok` variant of `Result`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), True)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_OK_VAL"), val)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_ERR_VAL"), NULL)

        return r

    @classmethod
    def err(cls, val: E) -> Result[T, E]:
        """Creates a new `Err` variant of `Result`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), False)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_OK_VAL"), NULL)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_ERR_VAL"), val)

        return r

    # ok or err

    def is_ok(self) -> bool:
        """Returns if self is an `Ok` variant"""
        return not not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_OK")
        )

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns `True` if self is an `Ok` variant and matches predicate"""
        if self.is_err():
            return False

        return f(self.unwrap())

    def is_err(self) -> bool:
        """Returns `True` if self is an `Err` variant"""
        return not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_OK")
        )

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        """Returns `False` if self is an `Err` variant and matches predicate"""
        if self.is_ok():
            return False

        return f(self.unwrap_err())

    # unwrap

    def unwrap(self) -> T:
        """
        If self is `Ok` variant, returns contained value

        If self is `Err` variant, panics
        """
        if self.is_err():
            panic("Called `Result.unwrap` on an `Err` variant")
        else:
            return object.__getattribute__(
                self, object.__getattribute__(self, "__INNER_OK_VAL")
            )

    def unwrap_or(self, val: T) -> T:
        """
        If self is `Ok` variant, returns contained value

        If self is `Err` variant, returns specified value
        """
        if self.is_err():
            return val
        else:
            return self.unwrap()

    def unwrap_or_else(self, f: Callable[[E], T]) -> T:
        """
        If self is `Ok` variant, returns contained value

        If self is `Err` variant, returns predicate result, passing it the err
        """
        if self.is_err():
            return f(self.unwrap_err())
        else:
            return self.unwrap()

    def unwrap_or_default(self, default: Default[T]) -> T:
        """
        If self is `Ok` variant, returns contained value

        If self is `Err` variant, returns default value for type
        """
        if self.is_err():
            return default.__default__()
        else:
            return self.unwrap()

    def unwrap_err(self) -> E:
        """
        If self is `Err` variant, returns contained value

        If self is `Ok` variant, panics
        """
        if self.is_ok():
            panic("Called `Result.unwrap_err` on an `Ok` variant")
        else:
            return object.__getattribute__(
                self, object.__getattribute__(self, "__INNER_ERR_VAL")
            )

    def expect(self, msg: str) -> T:
        """
        If self is `Ok` variant, returns the contained value

        If self is `Err` variant, panics with the specified error message
        """
        if self.is_err():
            panic(msg)
        else:
            return self.unwrap()

    def expect_err(self, msg: str) -> E:
        """
        If self is `Err` variant, returns the contained value

        If self is `Ok` variant, panics with the specified error message
        """
        if self.is_ok():
            panic(msg)
        else:
            return self.unwrap_err()

    # contains

    def contains(self, val: U) -> bool:
        """Returns whether the contained `Ok` value matches specified value"""
        if self.is_ok():
            return self.unwrap() == val
        else:
            return False

    def contains_err(self, val: F) -> bool:
        """Returns whether the contained `Err` value matches specified value"""
        if self.is_err():
            return self.unwrap_err() == val
        else:
            return False

    # map

    def map(self, f: Callable[[T], U]) -> Result[U, E]:
        """If self is an `Ok` variant, transform it with the predicate"""
        if self.is_ok():
            return Result.ok(f(self.unwrap()))
        else:
            return Result.err(self.unwrap_err())

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        If self is an `Ok` variant, transform it with the predicate

        If self is an `Err` variant, replace it with the value
        """
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """
        If self is an `Ok` variant, transform it with the predicate

        If self is an `Err` variant, replace it with the predicate value
        """
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default(self.unwrap_err())

    def map_err(self, f: Callable[[E], F]) -> Result[T, F]:
        """If self is an `Err` variant, transform it with the predicate f"""
        if self.is_ok():
            return Result.ok(self.unwrap())
        else:
            return Result.err(f(self.unwrap_err()))

    # inspect

    def inspect(self, f: Callable[[T], None]) -> Result[T, E]:
        """Calls a predicate on an `Ok` variant without modifying it"""
        if self.is_ok():
            f(self.unwrap())

            return Result.ok(self.unwrap())
        else:
            return Result.err(self.unwrap_err())

    def inspect_err(self, f: Callable[[E], None]) -> Result[T, E]:
        """Calls a predicate on an `Err` variant without modifying the value"""
        if self.is_ok():
            return Result.ok(self.unwrap())
        else:
            f(self.unwrap_err())

            return Result.err(self.unwrap_err())

    # iter

    def iter(self) -> Iterator[T]:
        """Transforms self into an iterator containing the `Ok` variant"""
        if self.is_ok():
            yield self.unwrap()

        return

    def iter_err(self) -> Iterator[E]:
        """Transforms self into an iterator containing the `Err` variant"""
        if self.is_err():
            yield self.unwrap_err()

        return
