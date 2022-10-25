
from functools import wraps
import time


def stopwatch(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"\n{func.__name__} took {end - start} seconds")

        return result

    return wrapper
