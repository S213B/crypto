import brk_fixed_iv_ctr
import my_rand
import ctr_mode
import base64
import xor_encrypt

def main():
    plains = []
    f = open("brk_fixed_iv_ctr2.txt", 'r')
    for line in f:
        plains.append(line)
    f.close()

    key = my_rand.my_rand_str(16)
    iv = 0
    ciphers = []
    for plain in plains:
        plain = base64.b64decode(plain)
        cipher = ctr_mode.ctr_encrypt(key, iv, plain)
        ciphers.append(cipher)

    key_stream = brk_fixed_iv_ctr.brk_fixed_iv_ctr(ciphers)

    import binascii
    print binascii.hexlify(key_stream)
    print binascii.hexlify(ctr_mode.ctr_encrypt(key, iv, chr(0)*max(map(len, ciphers))))
    #for i in range(len(ciphers)):
    #    cipher = ciphers[i]
    #    plain = plains[i]
    #    print xor_encrypt.xor_encrypt_str(cipher, key_stream)
    #    print base64.b64decode(plain)

if __name__ == "__main__":
    main()
