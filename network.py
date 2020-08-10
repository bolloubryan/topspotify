import socket

class Network:
	def __init__ (self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server="18.191.135.236"
		self.port=5555
		self.addr=(self.server, self.port)
		self.song = self.connect()

	def getSong (self):
		self.song = self.send("What's the song")
		return self.song

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except:
			print("no self")
			pass

	def send(self,data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()
		except socket.error as e:
			print(e)