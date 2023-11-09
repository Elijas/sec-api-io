from httpx._exceptions import HTTPStatusError
import random
import time

 
def retry_with_exponential_backoff(
    func,
    initial_delay: float = 0.1,
    exponential_base: float = 2,
    jitter: bool = True,
    max_retries: int = 10,
    errors: tuple = (HTTPStatusError,),
):

    def wrapper(*args, **kwargs):
        num_retries = 0
        delay = initial_delay
 
        # Loop until either a successful response 
        # or max_retries is hit  
        # or an unknown exception is raised
        while True:
            try:
                return func(*args, **kwargs)
 
            # Retry on specific errors
            except errors as e:
                num_retries += 1
                # Check if max retries has been reached
                if num_retries > max_retries:
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )
                # wait exponentially
                delay *= exponential_base * (1 + jitter * random.random())
                time.sleep(delay)
 
            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e
 
    return wrapper