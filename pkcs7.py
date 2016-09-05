import binascii

class BadPadError(Exception):
    pass

def pkcs7_pad(in_txt, block_size):
    l = len(in_txt)
    remainder = l % block_size
    padding = block_size - remainder
    return in_txt + chr(padding) * padding

def pkcs7_unpad(in_txt, block_size):
    padding = in_txt[-1]
    cnt = ord(padding)
    if len(in_txt) % block_size != 0:
        #print "text length", len(in_txt), "is not multiple of block size", block_size
        raise BadPadError
    if cnt > block_size:
        #print "padding size", cnt, "is larger than block size", block_size
        raise BadPadError
    if in_txt[-cnt:] != padding * cnt:
        #print "padding error", cnt
        raise BadPadError
    return in_txt[:-cnt]

if __name__ == "__main__":
    plaintext = "YELLOW SUBMARINE"
    text = pkcs7_pad(plaintext, 10)
    print binascii.hexlify(plaintext)
    print binascii.hexlify(text)

    str1 = 'abcdef'
    str2 = pkcs7_pad(str1, 16)
    str3 = str2[:-1] + chr(2)

    try:
        print pkcs7_unpad(str1, 16)
    except BadPadError as err:
        print "Bad Padding Format"

    print pkcs7_unpad(str2, 16)

    try:
        print pkcs7_unpad(str3, 16)
    except BadPadError as err:
        print "Bad Padding Format"

    for i in range(30):
        from my_rand import my_rand, my_rand_str
        raw_txt = my_rand_str(my_rand(213))
        pad_txt = pkcs7_pad(raw_txt, 16)
        unpad_txt = pkcs7_unpad(pad_txt, 16)
        if raw_txt != unpad_txt:
            print "PKCS7 Error"
