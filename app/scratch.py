


def my_decorator(func):
    def inner():
        print("\nSomething befor the execution of the func() we take as argument")
        func()
        print("Something after the we take the func() as argument\n")
    return inner

@my_decorator
def say_hello():
    print("\nHello world from say_hello func\n")


say_hello()