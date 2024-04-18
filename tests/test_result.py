from oxypy import Result


def test_is_ok_and_err() -> None:
    ok_res: Result[int, str] = Result.ok(42)
    err_res: Result[int, str] = Result.err("Hello World!")

    assert ok_res.is_ok() is True
    assert ok_res.is_err() is False

    assert err_res.is_ok() is False
    assert err_res.is_err() is True


def test_unwrap() -> None:
    ok_res: Result[int, str] = Result.ok(42)
    err_res: Result[int, str] = Result.err("Hello World!")

    assert ok_res.unwrap() == 42
    assert err_res.unwrap_err() == "Hello World!"
