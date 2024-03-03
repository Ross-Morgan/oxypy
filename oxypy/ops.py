from typing import Generic, Protocol, TypeVar


L_co = TypeVar("L_co", covariant=True)
R_co = TypeVar("R_co", contravariant=True)


class PartialEq(Protocol, Generic[L_co, R_co]):
    def __par_eq__(lhs: L_co, rhs: R_co):
        ...


class PartialOrd(Protocol, Generic[L_co, R_co]):
    def __par_ord__(lhs: L_co, rhs: R_co):
        ...
