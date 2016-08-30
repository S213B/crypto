import binascii
import aes_128_ecb

def detect_ecb_mode(line, block_len = 16):
    #print line
    #line = binascii.unhexlify(hex_line)
    blocks = aes_128_ecb.text_to_ecb_block(line, block_len)
    return len(blocks) - len(set(blocks))
    #print len(blocks), len(set(blocks))
    #if len(blocks) > len(set(blocks)):
        #print len(blocks), len(set(blocks))
        #print len(blocks)-len(set(blocks)), line
    #    return True
    #else:
    #    return False
    '''
    cnt = 0
    for i in range(len(blocks) - 1):
        if blocks[i] in blocks[i+1:]:
            cnt += 1
            print blocks[i]
    if cnt > 0:
        print cnt, line
    '''

if __name__ == '__main__':
    f = open('ecb_detect.txt', 'r')
    for line in f:
        _line = line.replace('\n', '')
        _line = binascii.unhexlify(_line)
        if detect_ecb_mode(_line) > 0:
            print "ECB detected"
            #print line
    f.close()
