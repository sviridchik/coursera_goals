import socket
import time
import json

class ClientError(Exception):
    pass
# raise ClientError("An error occurred")



class Client:
    def __init__(self,host,port,timeout):
        try:
            # self.sock = socket.socket()
            self.sock = socket.create_connection((host, port),timeout)
        #     settimeout??
        except socket.error as e:
            raise ClientError(f"Problems with connection : {e}")

    def put(self,name,body,timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        data_to_store = f"{name} {body} {timestamp}\n"
        try:
            self.sock.sendall(bytes("put "+data_to_store, encoding='UTF-8'))  # отправляем сообщение

        except socket.error as e:
            raise ClientError(f"Problems with sending : {e}")
        with open("storage", "w") as f:
            f.write(data_to_store)
        try:
            data = self.sock.recv(1024)  # читаем ответ от серверного сокета
        except socket.error as e:
            raise ClientError(f"Problems with response : {e}")
        data = data.decode().split("\n")
        status,data_processed  = data[0],data[1:len(data)-2]
        if status == "error":
            raise ClientError(data)
        # sock.close()  # закрываем соединение
        # print(data)

    def get(self,name):
        data_to_store = f"get {name}\n"
        try:
            self.sock.sendall(bytes(data_to_store, encoding='UTF-8'))  # отправляем сообщение
        except socket.error as e:
            raise ClientError(f"Problems with sending : {e}")
        try:
            data = self.sock.recv(1024)  # читаем ответ от серверного сокета
        except socket.error as e:
            raise ClientError(f"Problems with response : {e}")
        data = data.decode().split("\n")
        status, data_processed = data[0], data[1:len(data)-2]
        if status == "error":
            raise ClientError(data_processed)
        elif status != "ok":
            raise ClientError(data_processed)

        res = {}
        try:
            for el in data_processed:
                el = el.split()

                if len(el) == 1:
                    raise ClientError(data_processed,"herehere")

                # print(el)
                try:
                    if el[0] in res:
                        res[el[0]].append([int(el[2]),float(el[1])])
                    else:
                        res[el[0]] = [[int(el[2]),float(el[1])]]
                except Exception as e:
                    raise Exception(e)

            for k,v in res.items():
                res[k] = sorted(v, key=lambda el: el[0])
                res[k] = [tuple(el) for el in res[k]]

            return res
        except Exception:
            raise ClientError("here",data_processed,status)
    # for k,v in res.items():
    #     print(k,v)


