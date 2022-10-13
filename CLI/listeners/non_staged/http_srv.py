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

def create_new_UID():
	import string
	import random
	includes = string.ascii_letters + string.digits
	_len = 15
	return ''.join(random.choice(includes) for i in range(_len))

class Connection:
	def __init__(self, UID : str, MachineName : str, UserName : str):

		print(f"[{UID}] New Connection - {UserName}@{MachineName}")
		self.UID         = UID
		self.MachineName = MachineName
		self.UserName    = UserName

class MyServer(BaseHTTPRequestHandler):  

	def parse_init(self, headers):
		try:
			data = headers[header_name]
		except KeyError:
			print("[-] Key not found when trying to initialize connections. Please check")
			return None

		''' Cleaning the data '''
		new = [decrypt(i) for i in decrypt(data).split(',')]
		
		c = Connection(
			UID         = create_new_UID(),
			UserName    = new[0],
			MachineName = new[1]
		)

		connections.append(c)

		return c

	def valid_end(self, headers : dict = None):
		self.send_response(302)
		self.send_header("Content-type", "text/html")
		self.send_header(f"{header_prefix}-Allow", "Yes")

		if headers:
			for k,v in headers.items():
				self.send_header(k, v)

		# self.send_header(f"{header_prefix}-Connection", "Established")
		self.end_headers()

	def base(self, method):
		headers = parse_headers(self.headers)
		''' Checking for connection initialization '''
		if header_prefix in headers.keys():
			conn = self.parse_init(headers)
			if not conn:
				self.send_response(502)
				return

			self.valid_end(headers = { f"{header_prefix}-UID" : conn.UID })

		elif f'{header_prefix}-Response' in headers.keys():
			self.valid_end()

		elif f'{header_prefix}-Connection' in headers.keys():
			self.valid_end()

		else:
			self.valid_end()

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
	print(f"Initialized HTTP Listener @ http://{hostName}:{serverPort}")

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")