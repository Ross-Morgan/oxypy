import sys
import typing


def panic(*, msg: str) -> typing.NoReturn:
    print("Panicked:", msg, file=sys.stderr)
    sys.exit(1)
