import sys
import typing

class Panic(Exception):
    """
    A very basic Exception wrapper for Rust's `panic!()` functionality
    """
    def __init__(self, message: str) -> None:
        self.__message = message
        super().__init__()

    def __repr__(self) -> str:
        name = type(self).__name__
        message = self.__message

        return f"{name}({message!r})"

    def __call__(*args, **kwargs) -> typing.NoReturn:
        sys.exit_(1)


def panic(*, msg: str) -> typing.NoReturn:
    print("Panicked:", msg)
    sys.exit_(1)
