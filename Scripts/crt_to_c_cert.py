import sys

def crt_to_c(crt_file : str):
	try:
		with open(crt_file, 'rb') as f:
			data = f.read().hex()
	except FileNotFoundError:
		print("[!] Invalid file specified!")
		exit(1)
	except Exception as E:
		print(f"[!] An invalid error occurred: {E}")
		exit(1)

	data = [f"0x{i}" for i in [data[i:i + 2] for i in range(0, len(data), 2)]]
	cert_data = "const BYTE certData[] = { "
	for hex_item in data:
		cert_data += hex_item + ', '
	return cert_data[:-2] + " };"

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print(f"Invalid arguments specified!\nUsage: {sys.argv[0]} <.crt file>")
		exit(1)

	c_cert = crt_to_c(sys.argv[1])
	print(c_cert)
