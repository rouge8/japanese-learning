def not_none[T](val: T | None) -> T:
    if val is not None:
        return val
    else:
        raise AssertionError("value was None")


def exactly_one[T](val: list[T]) -> T:
    if len(val) != 1:
        raise AssertionError(f"value had length {len(val)}")
    return val[0]
