import asyncio


# <команда> <данные запроса><\n>
# <статус ответа><\n><данные ответа><\n\n>
class ClientError(Exception):
    pass


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


# loop = asyncio.get_event_loop()
# coro = loop.create_server(
#     ClientServerProtocol,
#     '127.0.0.1', 8181
# )
#
# server = loop.run_until_complete(coro)
#
# # try:
# #     loop.run_forever()
# # except KeyboardInterrupt:
# #     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()


class ClientServerProtocol(asyncio.Protocol):
    data_storage = {}

    # def craete_data_storage(self):
    #     # global data_storage
    #     self.data_storage = {}
    #     return

    def get(self, data_request):
        try:
            name = data_request.split()
            if len(name)>1:
                return 'error\nwrong command\n\n'
            name = name[0]
            if len(self.data_storage) == 0 or name not in self.data_storage:
                return 'ok\n\n'
            if name == "*":
                res = "ok\n"

                for k,v in self.data_storage.items():
                    for el in v:
                        res += f"{k} {el[0]} {el[1]}\n"
                res += "\n"
            else:
                res = "ok\n"
                for k, v in self.data_storage.items():
                    if k == name:
                        for el in v:
                            res += f"{k} {el[0]} {el[1]}\n"
                res += "\n"
                return res
        except Exception as e:
            return 'error\nwrong command\n\n'

    def put(self, data_request):
        try:
            if len(data_request.split()) != 3:
                return 'error\nwrong command\n\n'

            name, value, timestamp = data_request.split()
            value = float(value)
            timestamp = int(timestamp)
            # if name in self.data_storage and timestamp<self.data_storage[name][1]:
            #     return 'ok\n\n'
            if name not in self.data_storage:
                self.data_storage[name] = []
            else:
                # print(9)
                if timestamp not in  [el[1] for el in self.data_storage[name]] :
                    self.data_storage[name].append((value, timestamp))
                else:
                    for el in self.data_storage[name]:
                        if el[1] == timestamp:
                            el[0] = value
            return 'ok\n\n'
        except Exception as e:
            return 'error\nwrong command\n\n'

    def process_data(self, data):
        if len(data)<5 or data[-1] != "\n":
            return "error\nwrong command\n\n"
        requests = data.split("\n")[:-1]
        for req in requests:
            data_processed = req.split(maxsplit=1)
            if len(data_processed)==1:
                return 'error\nwrong command\n\n'

            command, data_request = data_processed[0], data_processed[1]
            if command == "get":
                resp = self.get(data_request)
                return resp
            elif command == "put":
                resp = self.put(data_request)
                return resp
            else:
                return "error\nwrong command\n\n"

    def connection_made(self, transport):
        # self.data_storage = self.craete_data_storage()
        super().__init__()
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

# run_server("127.0.0.1", 8889)
