__all__ = ["NULL"]


class Null:
    def __repr__(self) -> str:
        return "<NULL>"


NULL = Null()

Null.__new__ = lambda cls: Exception("Cannot create NULL")  # type: ignore
del Null
