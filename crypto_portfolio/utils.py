import time
from functools import wraps

def timing_decorator(func):
    """
    A decorator to measure the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if "quiet" is True
        if kwargs.get("quiet", False):
            # Call without timing
            return func(*args, **kwargs)
        
        #Measure execution time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        # Print Execution time
        print(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result
    
    return wrapper


    