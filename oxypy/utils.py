from typing import Generic, Protocol, Type, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Null:
    def __repr__(self) -> str:
        return "<NULL>"


class Panic(Exception):
    def __init__(self, message: str) -> None:
        self.__message = message
        super().__init__()

    def __repr__(self) -> str:
        name = type(self).__name__
        message = self.__message

        return f"{name}({message!r})"

class Default(Protocol, Generic[T_co]):
    @classmethod
    def default(cls: Type[T_co]) -> T_co:
        ...  # noqa


NULL = Null()
