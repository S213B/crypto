import random
import string
import aes_128_ecb
import cbc_mode
import pkcs7
import xor_encrypt
import base64
import ecb_detect

def my_rand(end, start = 0):
    num = int(random.random() * (end - start))
    return num + start

def my_rand_str(len):
    r = ''
    for i in range(len):
        while True:
            c = chr(my_rand(128))
            if c in string.printable:
                r += c
                break
    return r

def my_rand_byte(len):
    r = []
    for i in range(len):
        c = my_rand(256)
        r.append(c)
    return r

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
        cipher = aes_128_ecb.ecb_mode(aes_128_ecb.aes_128_encrypt, plain, key)
        print "encrypt mode: ECB"
    else:
        #cbc
        cipher = cbc_mode.cbc_encrypt(aes_128_ecb.aes_128_encrypt, iv, xor_encrypt.xor_encrypt_bin, plain, key)
        print "encrypt mode: CBC"

    #print base64.b64encode(cipher)

    if ecb_detect.ecb_detect(cipher):
        print "detect mode: ECB"
    else:
        print "detect mode: CBC"
        flag -= 1

    if flag == 0:
        print "Detect succeed"
    else:
        print "Detect failed"

if __name__ == '__main__':
    main()
