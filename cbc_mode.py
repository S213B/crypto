from xor_encrypt import *
from aes_128 import *
from ecb_mode import text_to_blocks
from pkcs7 import *
import binascii
import base64

def cbc_decrypt(decrypt_func, iv, cipher, key, size = 16, add_func = xor_encrypt_bin):
    plain = []
    cbc_blocks = text_to_blocks([ord(c) for c in cipher], size)
    for block in cbc_blocks:
        t_plain = decrypt_func(block, [ord(c) for c in key])
        plain += add_func(t_plain, iv)
        iv = block
    return pkcs7_unpad(''.join([chr(i) for i in plain]), size)

def cbc_encrypt(encrypt_func, iv, plain, key, size = 16, add_func = xor_encrypt_bin):
    plain = pkcs7_pad(plain, size)
    cipher = []
    cbc_blocks = text_to_blocks([ord(c) for c in plain], size)
    for block in cbc_blocks:
        block = add_func(block, iv)
        t_cipher = encrypt_func(block, [ord(c) for c in key])
        cipher += t_cipher
        iv = t_cipher
    return ''.join([chr(i) for i in cipher]) 

def main():
    f = open( "cbc_mode.txt", 'r' )
    b64_cipher = f.read()
    f.close()

    cipher = base64.b64decode( b64_cipher )
    iv = [0] * 16
    key = "YELLOW SUBMARINE"

    plain = cbc_decrypt(aes_128_decrypt, iv, cipher, key)
    #plain = pkcs7_unpad(plain, 16)
    
    print plain

'''
    #plain = pkcs7_pad(plain, 16)
    cipher = cbc_encrypt(aes_128_encrypt, iv, plain, key)

    b64_cipher = base64.b64encode( cipher )

    f = open( "tmp.txt", 'w' )
    f.write( b64_cipher )
    f.close()
    '''

if __name__ == "__main__":
    main()
