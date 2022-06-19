### This script decrypts the files affected by the Hemus encryption
### A decryption_key.pem is required to be in the same folder for this to work
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from base64 import b64decode

victim_pub_key = b''
victim_cipher = ''  # object
encrypted_using_asymmetric_keys_postfix = '.shhh'
encrypted_using_symmetric_keys_postfix = '.opalq'
assymetric_encrypted_victim_key_postfix = '.opa'
file_chunk_size = 2048
victim_key_size = 1024
target_directory = '\\Users\\'

# File extensions we identify for decryption
encrypted_extensions = [
    encrypted_using_asymmetric_keys_postfix, encrypted_using_symmetric_keys_postfix]
# File extensions we do not touch
do_not_encrypt = [encrypted_using_asymmetric_keys_postfix,
                  encrypted_using_symmetric_keys_postfix, assymetric_encrypted_victim_key_postfix]


# File extensions

# get file with symmeytic encryption
def get_symmetricly_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail + encrypted_using_symmetric_keys_postfix

# get file with asymmeytic encryption


def get_asymmetrically_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail + encrypted_using_asymmetric_keys_postfix


def get_original_symmetricly_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_symmetric_keys_postfix)


def get_original_asymmetrically_encrypted_absolute_path(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_asymmetric_keys_postfix)


def get_asymmetrically_encrypted_absolute_path_from_symmetrically_encrypted(absolute_path):
    head, tail = os.path.split(absolute_path)
    return head + '\\' + tail.removesuffix(encrypted_using_symmetric_keys_postfix) + encrypted_using_asymmetric_keys_postfix


def get_file_extension(file_name):
    return os.path.splitext(file_name)[1]

# Decrypt assymetricly encrypted files


def decrypt_asymmetric_key(absolute_encrypted_path, decryption_cipher):
    try:
        f = open(get_asymmetrically_encrypted_absolute_path_from_symmetrically_encrypted(
            absolute_encrypted_path), 'rb')
        encrypted_nonce_key = f.read()
        f.close()
        nonce_key = decryption_cipher.decrypt(encrypted_nonce_key)
        os.remove(get_asymmetrically_encrypted_absolute_path_from_symmetrically_encrypted(
            absolute_encrypted_path))
        return [nonce_key[:16], nonce_key[16:]]
    except:
        print('Asymmetric decryption failed')


def decrypt_symmetric_key(absolute_encrypted_path, key, nonce):
    aes_cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        f = open(absolute_encrypted_path, 'rb')
        d = open(get_original_symmetricly_encrypted_absolute_path(
            absolute_encrypted_path), 'wb')
        while True:
            src_data = f.read(file_chunk_size)  # 2 kb at a time
            if not src_data:  # ran out of data
                break
            d.write(aes_cipher.encrypt(src_data))
        f.close()
        d.close()
        os.remove(absolute_encrypted_path)
    except:
        print('Failed to decrypt')



def decrypt_file(absolute_encrypted_path, decryption_cipher):
    nonce_key = decrypt_asymmetric_key(
        absolute_encrypted_path, decryption_cipher)
    if nonce_key == None:
        print("failed to decrypt symmetric key")
        return None
    decrypt_symmetric_key(absolute_encrypted_path, nonce_key[1], nonce_key[0])


###

def decrypt_directory(absolute_path, cipher_decrpyption):
    for root, dirs, files in os.walk(absolute_path):
        for file in files:
            if (get_file_extension(file) == encrypted_using_symmetric_keys_postfix):
                decrypt_file(root + '\\' + file, cipher_decrpyption)


def import_decryption_key():
    try:
        f = open('decryption_key.pem', 'r')
        dec_key = f.read()
        f.close()
        return dec_key
    except:
        print('No key found!')
        return None

# set up


key__str = import_decryption_key()  # 'MIICXQIBAAKBgQCk4IOaYzCktT9K64pygYdQDgkWe8UcYUUr58qk9pSl9OMCVS6gRProp1kNLX5e5MWXmTOyVnhtjaupM3qWAT1XX2L6q0y2At5d1X93ztvEaC4r/u61J0Stv08tZlnIMbWTohabmT9k6jNNoRJ+L+KVJV7T+FhYIzhyPNFIuBgG5QIDAQABAoGABiRD2rgnq3cB7s9D1rya9wEy1vbQ0pwP+ND3VDpIMr9ixmc4Z6lyJED5mPtRGgVRE/LVwWalsUUF+DVN83ED4SJAP6zaX/kwSU8H+GLtQbQCYM5lflXU64j/5N/09x7pWoplO9ORMDb+Jt6ezBcs97U+fhu0PO3lmux5i2cTB2kCQQDGCQpZNs3H8XTxxjLnYPjoAWEgdH3MmHK4YLl+c/0YOf9KFJa9dQNMEMK7DM549WzrUbWc5JcMCBqNv/EA3T9tAkEA1SLkifkWcUU0rFN7E9KAE0qDvgRFolIdGMQMXjOKxzgoH7gr1icNQvgqZRL0sSBlQwW3BOBn6mHHVGp2xPKiWQJAPze5lvs4u8Anvdqwe05oht+R2uN1GS/9R0CRVn2+aNJy3XovGLHW6JxdHYscCl8GcyR1Xm1Wjp+zolaIn+cBDQJBAKKbjGD3ePfSJO2Ug0IMR0pwfzJpb/b3TtumNwlnqWl0nqgUit1HzgZZ735NiAHbBWas5YUC8EURdFIjJ5n6w4ECQQCET54ZJrUHb8AzaoFOgBDW9yFBABWR4LM0Q3NjmxiLjL0EDi7UXF+gVoT275KKNOzC+A9x6zzeLAQkY8Fq5+fr'

print(key__str)

key_dec = RSA.importKey(b64decode(key__str))
cipher_dec = PKCS1_OAEP.new(key_dec)

decrypt_directory(
    '\\Users', cipher_dec)
