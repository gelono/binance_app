import time
from functools import wraps


def measure_time(func):
    """
    Decorator that measures the execution time of a function every tenth time it is called and prints the result.

    Args:
        func (function): The function whose execution time needs to be measured.

    Returns:
        function: Wrapper around the `func` function, which measures its execution time.

    """
    count = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        if count % 10 == 0:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Method execute time {func.__name__}: {elapsed_time:.8f} second(s)")
            return result
        else:
            return func(*args, **kwargs)
    return wrapper
