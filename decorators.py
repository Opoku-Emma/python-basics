# Decorators have the ability to run additional code before
# and after each call to a function it wraps.
# They can also modify input arguments

from functools import wraps


def trace(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")

        return result
    return wrapper

@trace
def fibonacci(n: int):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci(n - 2) + fibonacci(n - 1))

fibonacci(3)

print(help(fibonacci))

# we need all information about the inner function to be
# captured in the outer function, so we use functools

def trace2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{func.__name__}({args!r}, {kwargs!r}) -> {result!r}")

        return result
    return wrapper

@trace2
def fibonacci2(n: int):
    """Return the n-th Fibonacci number"""
    if n in (0, 1):
        return n
    return (fibonacci2(n - 2) + fibonacci2(n - 1))

print(help(fibonacci2))