import aes_128
import ecb_mode
import struct
import xor_encrypt

# key    : str
# iv     : int
# in_txt : str
def ctr_mode(key, iv, in_txt, cipher_func = aes_128.aes_128_encrypt):
    out_txt = ''
    counter = 0
    key = map(ord, key)
    blocks = ecb_mode.text_to_blocks(in_txt, 16)
    for block in blocks:
        plain = struct.pack("<QQ", iv, counter)
        plain = map(ord, plain)
        cipher = cipher_func(plain, key)
        cipher = map(chr, cipher)
        out_txt += xor_encrypt.xor_encrypt_str(block, cipher)
        counter += 1
    return out_txt

# key    : str
# iv     : int
# in_txt : str
def ctr_encrypt(key, iv, in_txt, cipher_func = aes_128.aes_128_encrypt):
    return ctr_mode(key, iv, in_txt, cipher_func)

# key    : str
# iv     : int
# in_txt : str
def ctr_decrypt(key, iv, in_txt, cipher_func = aes_128.aes_128_encrypt):
    return ctr_mode(key, iv, in_txt, cipher_func)

def main():
    key = "YELLOW SUBMARINE"
    iv = 0
    cipher = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    import base64
    cipher = base64.b64decode(cipher)
    plain = ctr_decrypt(key, iv, cipher)
    print len(cipher), len(plain)
    print plain

if __name__ == "__main__":
    main()
