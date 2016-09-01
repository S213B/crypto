from __future__ import division
from ham_dis import ham_dis
from base64 import b64decode
from single_byte_xor_cipher import single_byte_xor_cipher
import binascii

def find_keysize(buff, max_keysize = 40):
    result = {}
    if len(buff) // 2 < max_keysize:
        max_keysize = len(buff) // 2
    for l in range(1, max_keysize):
        dis = ham_dis(buff[:l], buff[l:l*2])
        dis /= l
        result[l] = dis
    ret = sorted(result.iteritems(), key = lambda (k,v):(v,k))
    return ret

def rep_xor_decrypt(buff, keysize):
    result = ''
    _buff = []
    for i in range(keysize):
        _buff += ['']
        for j in range(i, len(buff), keysize):
            _buff[i] += buff[j]
        _buff[i], _score = single_byte_xor_cipher(binascii.hexlify(_buff[i]))
    for i in range(len(_buff[0])):
        for j in range(keysize):
            if i < len(_buff[j]):
                result += _buff[j][i]
    return result

if __name__ == '__main__':
    f = open('rep_xor_decrypt.txt', 'r')
    buff = f.read()
    buff = buff.replace('\n', '').replace('\r', '')
    buff = b64decode(buff)
    keysize = find_keysize(buff)
    #print keysize
    #top = 30
    #if len(keysize) < top:
    #    top = len(keysize)
    for i in range(len(keysize)):
        plain = rep_xor_decrypt(buff, keysize[i][0])
        if plain:
            print 'keysize:', keysize[i]
            print plain
