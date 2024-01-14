import time


def measure_speed(fn):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = fn(*args, **kwargs)
        end_time = time.time()
        print(f"Executing {fn.__name__} took {end_time - start_time} seconds.")
        return result

    return wrapper


# 例として使用するメソッド
@measure_speed
def example_function():
    for i in range(1000000):
        pass


if __name__ == '__main__':
    example_function()
