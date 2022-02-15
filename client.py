import socket
import time


class ClientError(Exception):
    pass
# raise ClientError("An error occurred")

sock = socket.socket()
sock.connect(("127.0.0.1", 10001))
message = "ping"
sock.sendall(message.encode("utf8"))
sock.close()

class Client:
    def __init__(self,host,port,timeout):
        try:
            self.sock = socket.socket()
            self.sock.connect((host, port),timeout)
        except socket.error as e:
            raise ClientError(f"Problems with connection : {e}")

    def put(self,name,body,timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())
        sock.send(bytes(body, encoding='UTF-8'))  # отправляем сообщение
        data = sock.recv(1024)  # читаем ответ от серверного сокета
        sock.close()  # закрываем соединение
        print(data)
