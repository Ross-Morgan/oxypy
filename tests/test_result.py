from oxypy import Result


def test_is_ok_and_err():
    ok_res = Result.ok(10)
    err_res = Result.err(20)

    assert ok_res.is_ok() is True
    assert ok_res.is_err() is False

    assert err_res.is_ok() is False
    assert err_res.is_err() is True


def test_unwrap():
    ok_res = Result.ok("Hello")
    err_res = Result.err("World")

    assert ok_res.unwrap() == "Hello"
    assert err_res.unwrap_err() == "World"
