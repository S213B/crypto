import aes_128
import ctr_mode
import ecb_mode
import my_rand
import xor_encrypt
import base64

def edit(cipher, key, iv, offset, new_plain):
    plain = ctr_mode.ctr_decrypt(key, iv, cipher)
    plain = plain[:offset] + new_plain
    return ctr_mode.ctr_encrypt(key, iv, plain)

def crk_rarw_aes_ctr(cipher, key, iv):
    new_plain = 'a' * len(cipher)
    new_cipher = edit(cipher, key, iv, 0, new_plain)
    key_stream = xor_encrypt.xor_encrypt_str(new_cipher, new_plain)
    plain = xor_encrypt.xor_encrypt_str(cipher, key_stream)
    return plain

def main():
    ecb_key = 'YELLOW SUBMARINE'
    f = open('aes_128.txt', 'r')
    cipher = base64.b64decode(f.read())
    f.close()
    plain = ecb_mode.ecb_decrypt(aes_128.aes_128_decrypt, cipher, ecb_key)

    key = my_rand.my_rand_str(16)
    iv = 0
    cipher = ctr_mode.ctr_encrypt(key, iv, plain)
    
    crk_plain = crk_rarw_aes_ctr(cipher, key, iv)
    
    if plain == crk_plain:
        print "crack succeed"
    else:
        print "crack failed"

if __name__ == "__main__":
    main()
