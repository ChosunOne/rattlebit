from hashlib import sha256, pbkdf2_hmac
from binascii import hexlify
from os import urandom

#Generate an SHA-2 hash
hash = sha256(b'Hello')
stringhash = hash.hexdigest()

#Generate a random set of bytes
nonce = urandom(32)

#Key Derivation
protected_hash = pbkdf2_hmac('sha256', b'angelisfat', nonce, 100000)
string_protected_hash = hexlify(protected_hash).decode()

print(hash.hexdigest())

# Sign a message with a digital signature
# message: the bytes of the message to be signed
# K: the private key to use for encrypting the signature
def signature(message, K, N, L):
    pass
    