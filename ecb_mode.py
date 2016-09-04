from pkcs7 import *

def text_to_blocks(text, size = 16):
    r = []
    for offset in range(0, len(text), size):
        r += [text[offset:offset+size]]
    return r

def ecb_mode(cipher_func, plain, key, size = 16):
    output = []
    ecb_blocks = text_to_blocks([ord(c) for c in plain], size)
    for block in ecb_blocks:
        output += cipher_func(block, [ord(c) for c in key])
    return ''.join([chr(i) for i in output])

def ecb_encrypt(cipher_func, plain, key, size = 16):
    plain = pkcs7_pad(plain, size)
    return ecb_mode(cipher_func, plain, key, size)

def ecb_decrypt(cipher_func, plain, key, size = 16):
    return pkcs7_unpad(ecb_mode(cipher_func, plain, key, size), size)
