import time
from http.server import HTTPServer, BaseHTTPRequestHandler

def decrypt(_ : str):
	from base64 import b64decode
	_ = _.encode()
	return b64decode(_).decode()

''' Variables '''
hostName = "0.0.0.0"
serverPort = 8080
header_name = "yTzbGtyzQEd"
header_prefix = "X-Raidware"

''' Don't change this code '''
connections = [  ]

def parse_headers(data):
	data = [i.strip().split(': ') for i in str(data).split('\n') if i != '']
	return {item[0] : item[1] for item in data}

def create_new_guid():
	import string
	import random
	includes = string.ascii_letters + string.digits
	_len = 8
	return ''.join(random.choice(includes) for i in range(_len))

class Connection:
	def __init__(self, GUID : str, MachineName : str, UserName : str):
		print(f"[{GUID}] New Connection - {UserName}@{MachineName}")
		self.GUID        = GUID
		self.MachineName = MachineName
		self.UserName    = UserName

class MyServer(BaseHTTPRequestHandler):  

	def parse_init(self, headers):
		try:
			data = headers[header_name]
		except KeyError:
			print("[-] Key not found when trying to initialize connections. Please check")
			return None

		_ = decrypt(data)
		''' Cleaning the data '''
		new = _.split(',')
		new = [decrypt(i) for i in new]
		c = Connection(
			GUID        = create_new_guid(),
			UserName    = new[0],
			MachineName = new[1]
		)
		connections.append(c)

		return True

	def base(self, method):

		headers = parse_headers(self.headers)
		''' Checking for connection initialization '''
		if 'Raidware' in headers.keys():
			if not self.parse_init(headers):
				self.send_response(502)
				return

			self.send_response(302)
			self.send_header("Content-type", "text/html")
			self.send_header(f"{header_prefix}-Allow", "Yes")
			self.send_header(f"{header_prefix}-Connection", "Established")
			self.end_headers()

		if f'{header_prefix}-Response' in headers.keys():
			pass

		if f'{header_prefix}-Connection' in headers.keys():
			pass

		self.wfile.write(bytes(f"Invalid request sent.", "utf-8"))

	def do_GET(self):
		self.base("GET")

	def do_PUT(self):
		self.base("PUT")

	def do_HEAD(self):
		self.base("HEAD")

	def do_POST(self):
		self.base("POST")

	def log_message(self, format, *args):
		return

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")