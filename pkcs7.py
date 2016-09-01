import binascii

class BadPadError(Exception):
    pass

def pkcs7_pad(input, block_size):
    l = len(input)
    remainder = l % block_size
    if remainder == 0:
        return input
    padding = block_size - remainder
    return input + chr(padding) * padding

def pkcs7_unpad(input, block_size):
    padding = input[-1]
    cnt = ord(padding)
    #if cnt >= block_size or len(input) % block_size != 0:
    if len(input) % block_size != 0:
        raise BadPadError
    if cnt >= block_size or input[-cnt:] != padding * cnt:
        #raise BadPadError
        return input
    return input[:-cnt]

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
