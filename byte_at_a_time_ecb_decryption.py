import base64
import aes_128_ecb
import string
import binascii
import my_rand
import ecb_detect

key = None

def encrypt_with_fixed_key(plain):
    #string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    string = "Um9sbGluJyBpbiBteSA1LjA="

    global key
    if key is None:
        key = my_rand.my_rand_str(16)
        #print len(base64.b64decode(string))

    plain = plain + base64.b64decode(string)

    return aes_128_ecb.ecb_mode(aes_128_ecb.aes_128_encrypt, plain, key)

def detect_block_size(encrypt_func):
    plain = ''
    cipher_len = len(encrypt_func(plain))
    pad_len = 0
    block_len = 1
    while True:
        plain += 'a'
        _cipher_len = len(encrypt_func(plain))
        if _cipher_len == cipher_len:
            pad_len += 1
        else:
            cipher_len = _cipher_len
            break
    while True:
        plain += 'a'
        _cipher_len = len(encrypt_func(plain))
        if _cipher_len == cipher_len:
            block_len += 1
        else:
            break
    return block_len, pad_len

def is_ecb_mode(encrypt_func, block_len, pad_len, block_cnt):
    # extra block_len for "xxaa aaaa aaax" pad_len overflow
    plain = 'a' * (pad_len + block_len * 3)
    cipher = encrypt_func(plain)
    if ecb_detect.detect_ecb_mode(cipher) > 0:
        return True
    else:
        return False

def make_one_byte_short_dic(encrypt_func, one_byte_short, offset_block = 0, pre_pad_len = 0):
    dic = {}
    block_len = len(one_byte_short) + 1
    offset = offset_block * block_len
    for c in range(256):#string.printable:
        c = chr(c)
        plain = 'a' * pre_pad_len + one_byte_short + c
        #print len(plain), plain
        key = encrypt_func(plain)[offset:offset + block_len]
        dic[key] = c
    return dic

def byte_at_a_time_ecb_decryption(encrypt_func):
    block_len, pad_len = detect_block_size(encrypt_func)
    print "block size:", block_len, "pad_len:", pad_len

    empty_len = len(encrypt_func(''))
    if empty_len % block_len != 0:
        print "Cannot detect block count"
        return None
    block_cnt = empty_len / block_len

    if not is_ecb_mode(encrypt_func, block_len, pad_len, block_cnt):
        print "Not ECB mode"
        return None
    else:
        print "Is ECB mode"

    r = ''
    one_byte_short = 'a' * (block_len * block_cnt - 1)
    for i in range(block_cnt * block_len - pad_len):
        _one_byte_short = (one_byte_short + r)[1-block_len:]
        #print len(_one_byte_short), _one_byte_short
        dic = make_one_byte_short_dic(encrypt_func, _one_byte_short)
        #print len(one_byte_short), one_byte_short
        cipher = encrypt_func(one_byte_short)
        #print len(cipher)
        #print cipher[: block_cnt*block_len]
        #print (block_cnt-1)*block_len, block_cnt*block_len
        cipher_block = cipher[(block_cnt-1)*block_len : block_cnt*block_len]
        c = dic[cipher_block]
        one_byte_short = one_byte_short[1:]
        r += c
        #print 'r=', r
    return r

def main():

    decrypted_text = byte_at_a_time_ecb_decryption(encrypt_with_fixed_key)

    if decrypted_text:
        print "succeed:"
        print decrypted_text
    else:
        print "failed"

if __name__ == "__main__":
    main()
