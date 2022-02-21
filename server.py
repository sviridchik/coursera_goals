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
            if name == "*":
                res = "ok\n"
                if len(self.data_storage)==0:
                    res += "\n"
                    return res
                for k, in self.data_storage.items():
                    res += f"{k} {self.data_storage[k][0]} {self.data_storage[k][0]} \n"
                res += "\n"
            else:
                res = f"ok\n{name} {self.data_storage[name][0]} {self.data_storage[name][0]} \n\n"
            return res
        except Exception as e:
            raise ClientError(e)

    def post(self, data_request):
        try:
            name, value, timestamp = data_request.split()
            value = float(value)
            timestamp = int(timestamp)
            self.data_storage[name] = (value, timestamp)
        except Exception as e:
            raise ClientError(e)

    def process_data(self, data):
        requests = data.split("\n")
        for req in requests:
            data_processed = req.split()
            command, data_request = data_processed[0], data_processed[1]
            if command == "get":
                self.get(data_request)
            elif command == "post":
                self.post(data_request)
            else:
                raise ClientError()

    def connection_made(self, transport):
        # self.data_storage = self.craete_data_storage()

        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())


