import socket
from _thread import *
import sys
from gettrack import * 

server ="192.168.56.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((server, port))
except socket.error as e:
	print(e)

s.listen(2)
print("Waiting for a connection, Sever Started")

def threaded_client(conn):
	conn.send(str.encode("hey user"))
	reply=WhatTrack()
	while (True):
		try:
			data=conn.recv(2048)
			recv=data.decode("utf-8")

			if not data:
				print("Disconnected")
				break
			else:
				print("Received: ", recv)
				print("Sending: ", reply)

			conn.sendall(str.encode(reply))
		except error as e:
			print(e)
			break

	print("Lost connection")
	conn.close()


while (True):
	conn, addr = s.accept()
	print("Connected to: ", addr)

	start_new_thread(threaded_client,(conn,))