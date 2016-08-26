from xor_encrypt import *
from aes_128_ecb import *
from pkcs7 import *
import binascii
import base64

def cbc_decrypt(decrypt_func, iv, rev_add_func, cipher, key, size = 16):
    plain = []
    cbc_blocks = text_to_ecb_block([ord(c) for c in cipher], size)
    for block in cbc_blocks:
        t_plain = decrypt_func(block, [ord(c) for c in key])
        plain += rev_add_func(t_plain, iv)
        iv = block
    return ''.join([chr(i) for i in plain])

def cbc_encrypt(encrypt_func, iv, add_func, plain, key, size = 16):
    plain = pkcs7_pad(plain, size)
    cipher = []
    cbc_blocks = text_to_ecb_block([ord(c) for c in plain], size)
    for block in cbc_blocks:
        block = add_func(block, iv)
        t_cipher = encrypt_func(block, [ord(c) for c in key])
        cipher += t_cipher
        iv = t_cipher
    return ''.join([chr(i) for i in cipher]) 

if __name__ == "__main__":
    f = open( "cbc_mode.txt", 'r' )
    b64_cipher = f.read()
    f.close()

    cipher = base64.b64decode( b64_cipher )
    iv = [0] * 16
    key = "YELLOW SUBMARINE"

    plain = cbc_decrypt(aes_128_decrypt, iv, xor_encrypt_bin, cipher, key)
    plain = pkcs7_unpad(plain, 16)
    
    print plain

'''
    #plain = pkcs7_pad(plain, 16)
    cipher = cbc_encrypt(aes_128_encrypt, iv, xor_encrypt_bin, plain, key)

    b64_cipher = base64.b64encode( cipher )

    f = open( "tmp.txt", 'w' )
    f.write( b64_cipher )
    f.close()
    '''
