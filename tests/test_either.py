from oxypy import Either


def test_is_left_and_right() -> None:
    left: Either[int, str] = Either.left(42)
    right: Either[int, str] = Either.right("Hello World!")

    assert left.is_left() is True
    assert left.is_right() is False

    assert right.is_left() is False
    assert right.is_right() is True


def test_unwrap() -> None:
    left: Either[int, str] = Either.left(42)
    right: Either[int, str] = Either.right("Hello World!")

    assert left.unwrap_left() == 42
    assert right.unwrap_right() == "Hello World!"
