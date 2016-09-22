import cbc_mode
import aes_128
import my_rand
import string
import xor_encrypt

cbc_key = my_rand.my_rand_str(16)
cbc_iv = map(ord, cbc_key)

def check_plain(plain):
    for c in plain:
        if c not in string.printable:
            return False
    return True

def encrypt(plain):
    return cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, cbc_iv, plain, cbc_key)

def decrypt(cipher):
    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, cbc_iv, cipher, cbc_key)
    return check_plain(plain), plain

def crk_cbc_iv_eq_key(decrypt_func, cipher, block_size = 16):
    block = 'a' * block_size
    zero = chr(0) * block_size
    crk_cipher = block + zero + block + cipher
    valid, crk_plain = decrypt_func(crk_cipher)
    return xor_encrypt.xor_encrypt_str(crk_plain[:block_size], crk_plain[block_size*2:block_size*3])

def main():
    plain = my_rand.my_rand_str(16)
    cipher = encrypt(plain)
    valid, _plain = decrypt(cipher)
    if valid and plain == _plain:
        print "works"
        # at least two blocks cipher text passed for padding validation in cbc decryption
        crk_key = crk_cbc_iv_eq_key(decrypt, cipher)
        if crk_key == cbc_key:
            print "crack"
        else:
            print cbc_key
            print crk_key
    else:
        print valid
        print plain
        print _plain

if __name__ == "__main__":
    main()
