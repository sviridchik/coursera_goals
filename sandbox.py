
# data = data.decode().split("\n")
data = "ok\npalm.cpu 2.0 1150864247\npalm.cpu 0.5 1150864248\neardrum.cpu 3.0 1150864250\n\n".split("\n")
status, data_processed = data[0], data[1:len(data)-2]
data_processed
print(status,data_processed)
if status == "error":
    raise Exception(data_processed)
else:
    res = {}
    for el in data_processed:
        el = el.split()
        # print(el)
        try:
            if el[0] in res:
                res[el[0]].append([int(el[2]) ,float(el[1])])
            else:
                res[el[0]] = [[int(el[2]) ,float(el[1])]]
        except Exception as e:
            raise Exception(e)

    for k ,v in res.items():
        res[k] = sorted(v, key=lambda el: el[0])
        res[k] = [tuple(el) for el in res[k]]
        print(res[k])
    # print(res)
