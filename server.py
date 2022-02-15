import socket
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 10001))   # max port 65535
sock.listen(socket.SOMAXCONN)
conn, addr = sock.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    # process data
    process_data = data.decode("utf8")
    # < команда > < данные запроса > <\n >
    print(process_data)
    command = process_data.split()[0]
    body = process_data.split()[1]

conn.close()
sock.close()
