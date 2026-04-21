def not_none[T](val: T | None) -> T:
    if val is not None:
        return val
    else:
        raise AssertionError("value was None")
