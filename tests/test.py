from rc4 import RC4
from base64 import b64encode, b64decode

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
    print("Testing: plaintext: ", plaintext)
    return plaintext.decode('latin-1')



print(decrypt(
    key="%sa2(soao@s",
    ciphertext="P7UxMMirBf97qlOKsRedms1lgOQqGaKkhyHoNUZF6ASpP/xoV/obB3yEvPTsjNMkZ47NyBMCwqmlKlShQWE4doRisXn4uAiAlJwEUC1iBzyjP/etmWDqrQe++arpESj3lOpjqv3zh3AdnZ6cQv9eIpfaLUbzc5j+pPCeLkwgeINzxU2mplku7x0R+5lPqg=="
))