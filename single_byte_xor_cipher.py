from __future__ import division
from xor2str import xor2str
import binascii
import string

def score_text(text):
    if not all(c in string.printable for c in text):
        return 0
    score = 0
    cnt = 0
    for c in text:
        if c in string.ascii_letters:
            cnt += 1
        if c is ' ':
            score += 0.1
    score += cnt / len(text)
#    parts = text.split(' ')
#    for part in parts:
#        if all(c in string.ascii_letters for c in part):
#            score += 1
#        if all(c in string.digits for c in part):
#            score += 1
    return score
    #return len(parts)


def single_byte_xor_cipher(cipher):
    '''
    input string is represented in hex
    '''
    if len(cipher) % 2 != 0:
        print 'length of input is', len(cipher)

    l = len(cipher) // 2

    score = 0
    result = ''
    for i in range(255):
        c = chr(i)
        key = binascii.hexlify(c) * l
        plain = xor2str(cipher, key)
        t_score = score_text(plain)
        #if t_score != 0:
        #    print t_score
        #    print plain
        if t_score > score:
            result = plain
            score = t_score
    #print score
    return result, score

if __name__ == '__main__':
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print single_byte_xor_cipher(s)
