from typing import Protocol


class Debug(Protocol):
    """
    A protocol that gives at type a user-friendly representation
    """
    def debug_string(self) -> str:
        ...


def dbg(*args: Debug, **kwargs: Debug):
    formatted_tuple = (str(v) for v in args)
    formatted_dict = (f"{k}={v.debug_string()}" for k, v in kwargs.items())

    print(*formatted_tuple, *formatted_dict)
