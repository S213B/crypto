import binascii

def xor2str(str1, str2):
    result = ''
    t_str1 = binascii.unhexlify(str1)
    #print t_str1
    t_str2 = binascii.unhexlify(str2)
    #print t_str2
    for idx in range(len(t_str1)):
        c = ord(t_str1[idx]) ^ ord(t_str2[idx])
        result += chr(c)
    return result

if __name__ == '__main__':
    s1 = '1c0111001f010100061a024b53535009181c'
    s2 = '686974207468652062756c6c277320657965'
    print xor2str(s1, s2)
