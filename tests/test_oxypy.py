from oxypy import Option, Result


def test_option_variant_validation():
    none_opt = Option.none()
    some_opt = Option.some(10)

    assert none_opt.is_none() is True
    assert none_opt.is_some() is False

    assert some_opt.is_none() is False
    assert some_opt.is_some() is True


def test_result_variant_validation():
    ok_res = Result.ok(10)
    err_res = Result.err(20)

    assert ok_res.is_ok() is True
    assert ok_res.is_err() is False

    assert err_res.is_ok() is False
    assert err_res.is_err() is True


def test_some_option_unwrapping():
    some_opt = Option.some(100)

    assert some_opt.unwrap() == 100
