import binascii

def xor_encrypt(plain, key):
    result = ''
    idx = 0
    for c in plain:
        result += chr(ord(c) ^ ord(key[idx]))
        idx = (idx + 1) % len(key)
    return result

def xor_encrypt_bin(plain, key):
    result = []
    idx = 0
    for c in plain:
        result += [c ^ key[idx]]
        idx = (idx + 1) % len(key)
    return result

if __name__ == '__main__':
    #s1 = "Burning 'em, if you ain't quick and nimble"
    #s2 = "I go crazy when I hear a cymbal"
    key = 'ICE'
    s3 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    #print len(s1), len(s2), len(s3)
    #print binascii.hexlify(xor_encrypt(s1, key))
    #print binascii.hexlify(xor_encrypt(s2, key))
    print binascii.hexlify(xor_encrypt(s3, key))
