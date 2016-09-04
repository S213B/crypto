import aes_128
import ecb_mode
import cbc_mode
import pkcs7
import xor_encrypt
import base64
import ecb_detect
from my_rand import *

def ecb_cbc_detect(cipher):
    if ecb_detect.detect_ecb_mode(cipher) > 0:
        print "detect mode: ECB"
        return True
    else:
        print "detect mode: CBC"
        return False


def main():
    f = open("ecb_cbc_detect.txt", 'r')
    plain = f.read()
    f.close()

    #print len(plain)
    plain = my_rand_str(my_rand(11, 5)) + plain
    plain += my_rand_str(my_rand(11, 5))
    #plain = pkcs7.pkcs7_pad(plain, 16)
    #print len(plain)

    key = my_rand_str(16)
    iv = my_rand_byte(16)
    flag = my_rand(2)
    cipher = ''

    if flag == 0:
        #ecb
        cipher = ecb_mode.ecb_encrypt(aes_128.aes_128_encrypt, plain, key)
        print "encrypt mode: ECB"
    else:
        #cbc
        cipher = cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, iv, xor_encrypt.xor_encrypt_bin, plain, key)
        print "encrypt mode: CBC"

    #print base64.b64encode(cipher)

    if not ecb_cbc_detect(cipher):
        flag -= 1

    if flag == 0:
        print "Detect succeed"
    else:
        print "Detect failed"

if __name__ == '__main__':
    main()
