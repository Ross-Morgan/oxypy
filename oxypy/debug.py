from typing import Protocol


class Debug(Protocol):
    """
    A protocol that gives at type a debug-friendly representation
    """
    def debug_string(self) -> str:
        ...


def dbg(args: list[Debug]):
    print(*map(Debug.debug_string, args))
