from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
from utils.rc4 import RC4
from utils.utils import json_fetch

class _AES:
    def __init__(self, key : str):
        BLOCK = 8
        if len(key) % BLOCK != 0:
            key = key + ''.join([key[i] for i in range(0, len(key) % BLOCK)])
        if type(key) != bytes:
            key = key.encode()
        self.key = key

    def encrypt(self, pt : str) -> str:

        if type(pt) != bytes:
            pt = pt.encode()

        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(pt, AES.block_size))
        return b64encode(cipher.iv + ct_bytes).decode()

    def decrypt(self, ct : str) -> str:

        if type(ct) == str:
            ct = ct.encode()

        enc = b64decode(ct)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(enc[AES.block_size:]).decode()

def quick_crypt(
    msg : str
):
    secret_key = json_fetch("Teamserver/config/config.json", "Raidware_Configuration")["SECRET_KEY"]
    return _AES(key=secret_key).encrypt(msg)

def quick_decrypt(
    ct : str
):
    if ct == None or ct == "":
        return None
        
    secret_key = json_fetch("Teamserver/config/config.json", "Raidware_Configuration")["SECRET_KEY"]
    return _AES(key=secret_key).decrypt(ct)

def SHA512(
    msg : str
):
    if type(msg) != bytes:
        msg = msg.encode()

    import hashlib
    return hashlib.sha512(msg).hexdigest()

def encrypt(
    key: bytes,
    plaintext: bytes,
) -> bytes:
    
    if(type(key) != bytes):
        key = key.encode()

    if(type(plaintext) != bytes):
        plaintext = plaintext.encode()

    rc4 = RC4(key)
    ciphertext = rc4.crypt(plaintext)
    return b64encode(ciphertext)

def decrypt(
    key: bytes,
    ciphertext: bytes,
) -> bytes:
    
    if(type(key) != bytes):
        key = key.encode()

    if(type(ciphertext) != bytes):
        ciphertext = ciphertext.encode()

    rc4 = RC4(key)
    plaintext = rc4.crypt(b64decode(ciphertext))
    return plaintext.decode('latin-1')

# Write me a function that will take as argument a string and then base64 encode it and then return md5 sum as a string:
def md5sum(
    msg : str
):
    if type(msg) != bytes:
        msg = msg.encode()

    import hashlib
    return hashlib.md5(msg).hexdigest()