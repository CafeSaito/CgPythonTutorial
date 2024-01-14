def my_decorator(func):
    def wrapper():
        print("何か前処理を行う")
        func()
        print("何か後処理を行う")

    return wrapper


@my_decorator
def say_hello():
    print("Hello!")


say_hello()
