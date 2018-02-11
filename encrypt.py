from Crypto.PublicKey import RSA
from geiger_trng import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

file_out = open("encrypted_data.bin", "wb")

data = b"hello world"

recipient_key = RSA.import_key(open("receiver.pub").read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
file_out.write(cipher_rsa.encrypt(session_key))

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[ file_out.write(x) for x in (cipher_aes.nonce, tag, ciphertext) ]
