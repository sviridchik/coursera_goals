# The decorator try to run function.
# If an error is raised, log error.

# 1. Write ErrorHandler decorator.
# a) as nested functions
def error_handler(f):
    log = []

    def wrapper(*args, **kwargs):
        print(args,kwargs)
        try:
            return f(*args, **kwargs)
        except Exception as e:
            log.append(e)
            print(e, log)

    return wrapper


# b) as class
class ErrorHandler:
    def __init__(self,f):
        self.f=f
        self.log = []

    def __call__(self, *args, **kwargs):
        # print(args,kwargs)
        try:
            return self.f(*args, **kwargs)
        except Exception as e:
            self.log.append(e)
            print(e, self.log)


# ============================================================================
# 2. Decorate this function using decorator
# a) with @
# @error_handler
@ErrorHandler
def handle_2a(raise_error=False):
    if raise_error:
        raise Exception("handle 2a")
    print("handle 2a")


handle_2a()
handle_2a(raise_error=True)


# b) without @
def handle_2b(raise_error=False):
    if raise_error:
        raise Exception("handle 2b")
    print("handle 2b")


error_handler(handle_2b)()
error_handler(handle_2b)(raise_error=True)


# # ============================================================================
# # 3. Add possibility to use decorator with or without parameter
# # a. error_handler - function, with parameter:
# @error_handler(label='input-data-validation')
# def handle_3a(raise_error=False):
#     if raise_error:
#         raise Exception("handle 3a")
#     print("handle 3a")
#
# handle_3a()
# handle_3a(raise_error=True)
#
# # b. error_handler - function, without parameter:
# @error_handler
# def handle_3b(raise_error=False):
#     if raise_error:
#         raise Exception("handle 3b")
#     print("handle 3b")
#
# handle_3b()
# handle_3b(raise_error=True)
#
#
# # c. ErrorHandler - class, with parameter:
# @ErrorHandler(label='input-data-validation')
# def handle_3c(raise_error=False):
#     if raise_error:
#         raise Exception("handle 3c")
#     print("handle 3c")
#
# handle_3c()
# handle_3c(raise_error=True)
#
# # d. ErrorHandler - class, without parameter:
# @ErrorHandler
# def handle_3d(raise_error=False):
#     if raise_error:
#         raise Exception("handle 3d")
#     print("handle 3d")
#
#
# handle_3d()
# handle_3d(raise_error=True)
