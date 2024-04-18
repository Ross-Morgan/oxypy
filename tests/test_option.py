from oxypy import Option


def test_is_none_and_some() -> None:
    none_opt = Option.none()
    some_opt = Option.some(42)

    assert none_opt.is_none() is True
    assert none_opt.is_some() is False

    assert some_opt.is_none() is False
    assert some_opt.is_some() is True


def test_unwrap() -> None:
    some_opt = Option.some(100)

    assert some_opt.unwrap() == 100
