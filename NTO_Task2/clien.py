import socket

client = socket.socket()
client.connect(('localhost', 1488))

while True:
	req = input('Enter message: ')
	client.send(req.encode())
	if req == 'close':
		break
	res = client.recv(1024)
	data = res.decode()
	print(data)

client.close()