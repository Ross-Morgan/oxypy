from __future__ import annotations

import os
from typing import Callable, Generic, Iterator, TypeVar

from .utils import NULL, Default, Panic

__all__ = ["Option"]

E = TypeVar("E")
F = TypeVar("F")

T = TypeVar("T")
U = TypeVar("U")
R = TypeVar("R")

T_co = TypeVar("T_co", covariant=True)


class Option(Generic[T], Default):
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
            return f"Some({self.unwrap()})"
        return "None"

    def __setattr__(self, _name, _val):
        return NotImplemented

    # defaults

    @classmethod
    def some(cls, val: T) -> Option[T]:
        """Creates new `Some` variant of `Option`"""
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), True)
        object.__setattr__(
            o, object.__getattribute__(cls, "__INNER_SOME_VAL"), val
        )

        return o

    @property
    @classmethod
    def none(cls) -> Option[T]:
        """Creates new `None` variant of `Option`"""
        o = cls()

        object.__setattr__(o, object.__getattribute__(cls, "__IS_SOME"), False)
        object.__setattr__(
            o, object.__getattribute__(cls, "__INNER_SOME_VAL"), NULL
        )

        return o

    @classmethod
    def default(cls) -> Option[T]:
        """Specifies default variant for `Option`"""
        return cls.none()

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
        return not not object.__getattribute__(
            self, object.__getattribute__(self, "__INNER_SOME_VAL")
        )

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        If self is `Some` variant and satisfies function, returns `True`

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

        If self is `None` variant, returns result of specified function
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
            raise Panic("Called `Option.unwrap` on a `None` value")
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

    # TODO Docs

    def unwrap_or_default(self, default: Default[T]) -> T:
        return self.unwrap_or(default.default())

    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, returns result of specified function
        """
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
        """ """
        if self.is_none():
            return Result.err(default)

        return Result.ok(self.unwrap())

    # get

    def get_or_insert(self, val: T) -> T:
        """
        If self is `Some` variant, returns contained value
        If self is `None` variant, sets to and returns specified value
        """
        if self.is_some():
            return self.unwrap()

        object.__setattr__(self, object.__setattr__(self, "__IS_SOME"), True)
        object.__setattr__(
            self, object.__setattr__(self, "__INNER_SOME_VAL"), val
        )

        return val

    def get_or_insert_default(self, default: Default) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, sets to and returns default for type
        """
        return self.get_or_insert(default.default())

    def get_or_insert_with(self, f: Callable[[], T]) -> T:
        """
        If self is `Some` variant, returns contained value

        If self is `None` variant, sets to and returns function result
        """
        return self.get_or_insert(f())

    # replace

    def replace(self, val: T) -> Option[T]:
        """Make self `Some` variant by replacing existing value"""
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(
            self, object.__getattribute__(self, "__IS_SOME"), True
        )  # noqa
        object.__setattr__(
            self, object.__getattribute__(self, "__INNER_SOME_VAL"), val
        )  # noqa

        return inner

    # take

    def take(self) -> Option[T]:
        """Returns copy of self, and makes self `None`"""
        if self.is_some():
            inner = Option.some(self.unwrap())
        else:
            inner = Option.none()

        object.__setattr__(
            self, object.__getattribute__(self, "__IS_SOME"), False
        )  # noqa
        object.__setattr__(
            self, object.__getattribute__(self, "__INNER_SOME_VAL"), NULL
        )  # noqa``

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
            return Option.none

        return Option.some(
            (
                self.unwrap(),
                other.unwrap(),
            )
        )

    def zip_with(self, other: Option[U], f: Callable[[T, U], R]) -> Option[R]:
        """Zips `self` and `other` with the specified function"""
        if not (self.is_some() and other.is_some()):
            return Option.none

        return Option.some(f(self.unwrap(), other.unwrap()))


class Result(Generic[T, E]):
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
        """Creates a new `Ok` variant of `Result`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), True)
        object.__setattr__(
            r, object.__getattribute__(cls, "__INNER_OK_VAL"), val
        )  # noqa
        object.__setattr__(
            r, object.__getattribute__(cls, "__INNER_ERR_VAL"), NULL
        )  # noqa

        return r

    @classmethod
    def err(cls, val: E) -> Result[T, E]:
        """Creates a new `Err` variant of `Result`"""
        r = cls()

        object.__setattr__(r, object.__getattribute__(cls, "__IS_OK"), False)
        object.__setattr__(
            r, object.__getattribute__(cls, "__INNER_OK_VAL"), NULL
        )  # noqa
        object.__setattr__(
            r, object.__getattribute__(cls, "__INNER_ERR_VAL"), val
        )  # noqa

        return r

    # ok or err

    def is_ok(self) -> bool:
        """Returns if self is an `Ok` variant"""
        return not not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_OK")
        )

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns if self is an `Ok` variant and satifies a function"""
        if self.is_err():
            return False

        return f(self.unwrap())

    def is_err(self) -> bool:
        """Returns if self is an `Err` variant"""
        return not object.__getattribute__(
            self, object.__getattribute__(self, "__IS_OK")
        )

    def is_err_and(self, f: Callable[[E], bool]) -> bool:
        """Returns if self is an `Err` variatn adn satisfies a function"""
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
            raise Panic("Called `Result.unwrap` on an `Err` variant")
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

        If self is `Err` variant, returns function result, passing it the err
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
            return default.default()
        else:
            return self.unwrap()

    def unwrap_err(self) -> E:
        """
        If self is `Err` variant, returns contained value

        If self is `Ok` variant, panics
        """
        if self.is_ok():
            raise Panic("Called `Result.unwrap_err` on an `Ok` variant")
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
            raise Panic(msg)
        else:
            return self.unwrap()

    def expect_err(self, msg: str) -> E:
        """
        If self is `Err` variant, returns the contained value

        If self is `Ok` variant, panics with the specified error message
        """
        if self.is_ok():
            raise Panic(msg)
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
        """If self is an `Ok` variant, transform it with the function"""
        if self.is_ok():
            return Result.ok(f(self.unwrap()))
        else:
            return Result.err(self.unwrap_err())

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        If self is an `Ok` variant, transform it with the function

        If self is an `Err` variant, replace it with the value
        """
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default

    def map_or_else(self, default: Callable[[E], U], f: Callable[[T], U]) -> U:
        """
        If self is an `Ok` variant, transform it with the function

        If self is an `Err` variant, replace it with the function value
        """
        if self.is_ok():
            return f(self.unwrap())
        else:
            return default()

    def map_err(self, f: Callable[[E], F]) -> Result[T, F]:
        """If self is an `Err` variant, transform it with the function f"""
        if self.is_ok():
            return Result.ok(self.unwrap())
        else:
            return Result.err(f(self.unwrap_err()))

    # inspect

    def inspect(self, f: Callable[[T], None]) -> Result[T, E]:
        """Calls a function on an `Ok` variant without modifying it"""
        if self.is_ok():
            f(self.unwrap())

            return Result.ok(self.unwrap())
        else:
            return Result.err(self.unwrap_err())

    def inspect_err(self, f: Callable[[E], None]) -> Result[T, E]:
        """Calls a function on an `Err` variant without modifying the value"""
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
