def my_decorator(func):
    def wrapper(*args, **kwargs):
        arg1 = args[0]
        print(f"{arg1}に関する、何か前処理を行う")
        result = func(*args, **kwargs)
        print(f"{arg1}に関する、何か後処理を行う")
        return result

    return wrapper


@my_decorator
def greet(name):
    print(f"Hello {name}!")


if __name__ == '__main__':
    greet("Alice")
