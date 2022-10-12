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

''' Don't change this code '''
connections = [  ]

def parse_headers(data):
	data = [i.strip().split(': ') for i in str(data).split('\n') if i != '']
	return {item[0] : item[1] for item in data}

class Connection:
	def __init__(
		self,
		GUID        : str,
		MachineName : str,
		UserName    : str
	):
		print(f"[{GUID}] New Connection - {UserName}@{MachineName}")
		self.GUID = GUID
		self.MachineName = MachineName
		self.UserName = UserName

class MyServer(BaseHTTPRequestHandler):  

	def parse_init(self, headers):
		try:
			data = headers[header_name]
		except KeyError:
			print("[-] Key not found when trying to initialize connections. Please check")
			return None

		_ = decrypt(data)
		''' Cleaning the data '''


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
		self.send_header("X-Raidware-Allow", "Yes")
		self.send_header("X-Raidware-Connection", "Established")
		self.end_headers()
		self.wfile.write(bytes(f"Invalid request sent.", "utf-8"))

	def do_GET(self):
		self.base("GET")

	def do_PUT(self):
		self.base("PUT")

	def do_HEAD(self):
		self.base("HEAD")

	def do_POST(self):
		self.base("POST")

if __name__ == "__main__":
	webServer = HTTPServer((hostName, serverPort), MyServer)
	print("Server started http://%s:%s" % (hostName, serverPort))  #Server starts

	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()  #Executes when you hit a keyboard interrupt, closing the server
	print("Server stopped.")