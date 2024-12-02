import os
import time
from time import sleep


def load_data(file_name):
    input_path = os.path.join(os.path.dirname(__file__), f'../inputs/{file_name}')
    with open(input_path, 'r') as file:
        data = file.read()
    return data

def time_decorator(func):
    def wrapper(*args, **kwargs):
        # start_cpu = time.process_time()
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        # end_cpu = time.process_time()
        end_time = time.perf_counter()
        result_time = end_time - start_time
        print(f"{func.__name__} needed {result_time:.6f} seconds.")
        return result  # Func result
    return wrapper