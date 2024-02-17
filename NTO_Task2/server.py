import socket

sock = socket.socket()

sock.bind(('', 1488))
sock.listen(1)

conn, addr = sock.accept()
print('connected:', addr)

while True:
	data = conn.recv(1024)
	message = data.decode()
	if message == 'close':
		break
	print(data)
	res = message.encode()
	conn.send(res.upper())

conn.close()