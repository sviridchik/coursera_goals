import asyncio
import logging

# <команда> <данные запроса><\n>
# <статус ответа><\n><данные ответа><\n\n>

# logging.basicConfig(level="DEBUG")


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    logging.info("Start accept connections")
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info("Exit")

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):

    def get(self, data_request):
        logging.info("Run get command, data=%s", data_request)
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
            storage = self.data_storage.setdefault(name, [])

            timestamps = {t for _, t in storage}
            if timestamp not in timestamps:
                storage.append((value, timestamp))
            else:
                storage.append((value, timestamp))
                self.data_storage[name] = list(set(storage))
            return 'ok\n\n'
        except Exception as e:
            return 'error\nwrong command\n\n'

    def process_data(self, data):
        logging.info("Process data, %s", data)

        if len(data)<5 or data[-1] != "\n":
            return "error\nwrong command\n\n"

        requests = data.split("\n")[:-1]
        for req in requests:
            logging.info("Process request, %s", req)

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
        self.data_storage = {}
        logging.info("Connection created, %s", transport)
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

#
# if __name__ == "__main__":
#     run_server("127.0.0.1", 8888)
