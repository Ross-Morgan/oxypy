from __future__ import annotations

import os
from typing import Callable, Generic, TypeVar

from .default import Default
from .panic import Panic
from .utils import NULL

__all__ = ["Either"]

L = TypeVar("L")
R = TypeVar("R")

C = TypeVar("C")
T = TypeVar("T")

K = TypeVar("K")
S = TypeVar("S")


class Either(Generic[L, R]):
    """
    Class containing either an `Left(L)` or `Right(R)` variant

    Used for expressing where a value may be one of two types
    """

    vars()["__RAND_LEN"] = 64
    vars()["__IS_LEFT"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )
    vars()["__INNER_LEFT_VAL"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )
    vars()["__INNER_RIGHT_VAL"] = (
        os.urandom(vars()["__RAND_LEN"])
        .decode(errors="ignore")
        .center(vars()["__RAND_LEN"] + 2)
    )

    def __repr__(self) -> str:
        if self.is_left():
            return f"Left({self.unwrap_left()})"
        else:
            return f"Right({self.unwrap_right()})"

    def __str__(self) -> str:
        return self.__repr__()

    def __setattr__(self, _name, _value) -> None:
        raise NotImplementedError

    # defaults

    @classmethod
    def left(cls, val: L) -> Either[L, R]:
        """Creates a new `Left` variant of `Either`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_LEFT"), True)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_LEFT_VAL"), val)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_RIGHT_VAL"), NULL)

        return r

    @classmethod
    def right(cls, val: R) -> Either[L, R]:
        """Creates a new `Right` variant of `Either`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_LEFT"), False)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_LEFT_VAL"), NULL)
        object.__setattr__(r, object.__getattribute__(cls, "__INNER_RIGHT_VAL"), val)

        return r

    # ok or err

    def is_left(self) -> bool:
        """Returns `True` if self is `Left` variant"""
        return not not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_LEFT")
        )

    def is_right(self) -> bool:
        """Returns `True` if self is `Right` variant"""
        return not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_LEFT")
        )

    # unwrap

    def unwrap_left(self) -> L:
        """
        If self is `Left` variant, returns contained value

        If self is `Right` variant, panics
        """
        if self.is_right():
            raise Panic("Called `Either.unwrap_left` on a `Right` variant")
        else:
            return object.__getattribute__(
                self, object.__getattribute__(self, "__INNER_LEFT_VAL")
            )

    def unwrap_right(self) -> R:
        """
        If self is `Left` variant, panics

        If self is `Right` variant, returns contained value
        """
        if self.is_left():
            raise Panic("Called `Either.unwrap_right` on a `Left` variant")
        else:
            return object.__getattribute__(
                self, object.__getattribute__(self, "__INNER_RIGHT_VAL")
            )

    # expect

    def expect_left(self, msg: str) -> L:
        """
        If self is `Left` variant, returns the contained value

        If self is `Right` variant, panics with the specified error message
        """
        if self.is_right():
            raise Panic(msg)
        else:
            return self.unwrap_left()

    def expect_right(self, msg: str) -> R:
        """
        If self is `Left` variant, panics with the specified error message

        If self is `Right` variant, returns the contained value
        """
        if self.is_left():
            raise Panic(msg)
        else:
            return self.unwrap_right()

    # either

    def either(self, f: Callable[[L], T], g: Callable[[R], T]) -> T:
        """
        If self is `Left` variant, return the contained value wrapped in `f`

        If self is `Right` variant, returns the contained value wrapped in `g`
        """
        if self.is_left():
            return f(self.unwrap_left())
        else:
            return g(self.unwrap_right())

    def either_with(self, ctx: C, f: Callable[[C, L], T], g: Callable[[C, R], T]) -> T:
        """
        If self is `Left` variant, return the contained value wrapped in `f`

        If self is `Right` variant, returns the contained value wrapped in `g`

        Like `Either.either` but supplies extra context to which function
        ends up being called
        """
        if self.is_left():
            return f(ctx, self.unwrap_left())
        else:
            return g(ctx, self.unwrap_right())

    # and then

    def left_and_then(self, f: Callable[[L], K]) -> Either[K, R]:
        """
        If self is `Left` variant, wraps the value in `f`

        If self is `Right` variant, returns a copy of self
        """
        inner: Either[K, R]

        if self.is_left():
            inner = Either.left(f(self.unwrap_left()))
        else:
            inner = Either.right(self.unwrap_right())

        return inner

    def right_and_then(self, g: Callable[[R], S]) -> Either[L, S]:
        """
        If self is `Left` variant, returns a copy of self

        If self is `Right` variant, wraps the value in `f`
        """
        inner: Either[L, S]

        if self.is_left():
            inner = Either.left(self.unwrap_left())
        else:
            inner = Either.right(g(self.unwrap_right()))

        return inner

    # or

    def left_or(self, other: L) -> L:
        """
        If self is `Left` variant, returns contained value

        If self is `Right` variant, returns given value
        """
        if self.is_left():
            return self.unwrap_left()
        else:
            return other

    def left_or_default(self, default: Default[L]) -> L:
        """
        If self is `Left` variant, returns contained value

        If self is `Right` variant, returns type's default value
        """
        if self.is_left():
            return self.unwrap_left()
        else:
            return default.default()

    def left_or_else(self, g: Callable[[R], L]) -> L:
        """
        If self is `Left` variant, returns contained value

        If self is `Right` variant, returns result of given function `f`
        """
        if self.is_left():
            return self.unwrap_left()
        else:
            return g(self.unwrap_right())

    def right_or(self, other: R) -> R:
        """
        If self is `Left` variant, returns given value

        If self is `Right` variant, returns contained value
        """
        if self.is_right():
            return self.unwrap_right()
        else:
            return other

    def right_or_default(self, default: Default[R]) -> R:
        """
        If self is `Left` variant, returns type's default value

        If self is `Right` variant, returns contained value
        """
        if self.is_right():
            return self.unwrap_right()
        else:
            return default.default()

    def right_or_else(self, f: Callable[[L], R]) -> R:
        """
        If self is `Left` variant, returns result of given function `f`

        If self is `Right` variant, returns contained value
        """
        if self.is_right():
            return self.unwrap_right()
        else:
            return f(self.unwrap_left())
