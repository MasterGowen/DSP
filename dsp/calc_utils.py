import numpy as np


def arrays_is_equal(x, y, tolerance=0.01):
    return np.allclose(x, y, atol=tolerance)


def numbers_is_equal(x, y, tolerance=0.5, rel=0.00005):
    if tolerance is rel is None:
        raise TypeError('cannot specify both absolute and relative errors are None')
    tests = []
    if tolerance is not None: tests.append(tolerance)
    if rel is not None: tests.append(rel * abs(x))
    assert tests
    return abs(x - y) <= max(tests)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z