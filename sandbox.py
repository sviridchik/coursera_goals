# import os
#
# photo_file_name="1.jpg"
# root, ext = os.path.splitext(photo_file_name)
# print(root,ext)
data_storage={"a":[(10,3),(5,4)],"b":[(19,18)]}
# print(len(data_storage))
res = ""

for k,v in data_storage.items():
    # print(k,v)
    for el in v:
        res += f"{k} {el[0]} {el[1]}\n"

print(res)
