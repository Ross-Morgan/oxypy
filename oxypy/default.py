from typing import Generic, Protocol, Type, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Default(Protocol, Generic[T_co]):
    """
    A protocol that gives a type the ability to have a default value
    """
    @classmethod
    def __default__(cls: Type[T_co]) -> T_co:
        ...
