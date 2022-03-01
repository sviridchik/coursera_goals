# # import os
# #
# # photo_file_name="1.jpg"
# # root, ext = os.path.splitext(photo_file_name)
# # print(root,ext)
# data_storage={"a":[(10,3),(5,4)],"b":[(19,18)]}
# # print(len(data_storage))
# res = ""
#
# for k,v in data_storage.items():
#     # print(k,v)
#     for el in v:
#         res += f"{k} {el[0]} {el[1]}\n"
#
# print(res)

class Decorator:
    def __init__(self, func):
        print('> Класс Decorator метод __init__')
        self.func = func

    def __call__(self):
        print('> перед вызовом класса...', self.func.__name__)
        self.func()
        print('> после вызова класса')

@Decorator
def wrapped():
    print('функция wrapped')

print('>> старт')
wrapped()
print('>> конец')
