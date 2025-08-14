import functools
from fastapi import Depends

def log_dependency():
    print("[Dependency] Before endpoint execution")

# Custom decorator example (runs before and after endpoint execution)
def log_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        print("[Decorator] Before endpoint execution")
        result = await func(*args, **kwargs)
        print("[Decorator] After endpoint execution")
        return result
    return wrapper
