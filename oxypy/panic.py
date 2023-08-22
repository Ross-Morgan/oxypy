class Panic(Exception):
    def __init__(self, message: str) -> None:
        self.__message = message
        super().__init__()

    def __repr__(self) -> str:
        name = type(self).__name__
        message = self.__message

        return f"{name}({message!r})"
