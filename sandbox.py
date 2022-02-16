

data = 'error\nwrong command\n\n'
data = data.split("\n")
status, data = data[0], data[1:len(data)-2]
print(status, data, "error" == status)
if status == "error":
    print("a")

    raise Exception()
    # raise ClientError(data)
    # res = {}
# for el in data:
#     el = el.split()
#     # print(el)
#     try:
#         if el[0] in res:
#             res[el[0]].append([int(el[2]),float(el[1])])
#         else:
#             res[el[0]] = [[int(el[2]),float(el[1])]]
#     except Exception as e:
#         raise Exception(e)
#
# for k,v in res.items():
#     res[k] = sorted(v, key=lambda el: el[0])
# print(res)
# # for k,v in res.items():
# #     print(k,v)
