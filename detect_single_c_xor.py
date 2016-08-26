from single_byte_xor_cipher import single_byte_xor_cipher
import binascii

def detect_single_c_xor(file_name, cnt):
    f = open(file_name, 'r')
    
    score = 0
    result = ''
    for line in f:
        line = line.replace('\r', '').replace('\n', '')
        if len(line) != cnt:
            continue
        plain, _score = single_byte_xor_cipher(line)
        #if _score != 0:
        #    print plain, _score
        if _score > score:
            result = plain
            score = _score

    f.close()

    return result

if __name__ == '__main__':
    print detect_single_c_xor('detect_single_c_xor.txt', 60)
