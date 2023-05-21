from magik import Result


def could_fail(x: int) -> Result[int, str]:
    if x == 0:
        return Result.err(f"Cannot divide {x!r} by 0")
    else:
        return Result.ok(100 / x)


def main():
    res_a = could_fail(10)
    res_b = could_fail(1)
    res_c = could_fail(0)

    print(f"{res_a = }")
    print(f"{res_b = }")
    print(f"{res_c = }")


if __name__ == "__main__":
    main()
