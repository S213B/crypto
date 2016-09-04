from byte_at_a_time_ecb_decryption import detect_block_size, is_ecb_mode, make_one_byte_short_dic
from my_rand import my_rand, my_rand_str
from aes_128 import aes_128_encrypt
from ecb_detect import detect_ecb_mode
import ecb_mode

key = my_rand_str(16)
#prefix_str = my_rand_str(my_rand(213))
#suffix_str = my_rand_str(my_rand(213))
prefix_str = my_rand_str(my_rand(32))
suffix_str = my_rand_str(my_rand(32))
#print "prefix string length:", len(prefix_str)
#print "suffix string length:", len(suffix_str)

def encrypt_with_fixed_key(plain):

    plain = prefix_str + plain + suffix_str

    return ecb_mode.ecb_encrypt(aes_128_encrypt, plain, key)

def detect_offset_block(encrypt_func, block_len, pad_len):
    # extra block_len for "xxaa aaaa aaax" pad_len overflow
    test_in = 'a' * (pad_len + block_len * 3)
    test_out = encrypt_func(test_in)
    for i in range(len(test_out) / block_len):
        part_1 = test_out[i*block_len : (i+1)*block_len]
        part_2 = test_out[(i+1)*block_len : (i+2)*block_len]
        #print i, len(test_out)
        #print part_1
        #print part_2
        if part_1 == part_2:
            return i
    return -1

def detect_pre_pad_len(encrypt_func, block_len, offset_block):
    pre_pad_len = 0
    test_in = 'a' * block_len * 2 + 'b' # append 'b' in case of the first byte of suffix string is 'a'
    while True:
        test_out = encrypt_func(test_in)
        part_1 = test_out[offset_block*block_len : (offset_block+1)*block_len]
        part_2 = test_out[(offset_block+1)*block_len : (offset_block+2)*block_len]
        if part_1 == part_2:
            return pre_pad_len
        test_in = 'a' + test_in # prepend 'a', otherwise loop never stop
        pre_pad_len += 1
        #print pre_pad_len
        #print test_in
    return -1

def byte_at_a_time_ecb_decryption2(encrypt_func):
    block_len, pad_len = detect_block_size(encrypt_func)
    print "block size:", block_len, "pad_len:", pad_len

    empty_len = len(encrypt_func(''))
    if empty_len % block_len != 0:
        print "Cannot detect block count"
        return None
    block_cnt = empty_len / block_len
    print "block_cnt:", block_cnt

    if not is_ecb_mode(encrypt_func, block_len, pad_len):
        print "Not ECB mode"
        return None
    else:
        print "Is ECB mode"

    offset_block = detect_offset_block(encrypt_func, block_len, pad_len)
    if offset_block < 0:
        print "Cannot detect offset block count"
        return None
    print "offset_block:", offset_block

    pre_pad_len = detect_pre_pad_len(encrypt_func, block_len, offset_block)
    suf_pad_len = pad_len - pre_pad_len
    if suf_pad_len < 0:
        suf_pad_len += block_len
    print "pre_pad_len:", pre_pad_len, "suf_pad_len:", suf_pad_len

    r = ''
    one_byte_short = 'a' * (pre_pad_len + block_cnt * block_len - 1)
    for i in range(block_cnt * block_len - offset_block * block_len - (pad_len - pre_pad_len)):
        _one_byte_short = (one_byte_short + r)[1-block_len:]
        #print len(_one_byte_short), _one_byte_short
        dic = make_one_byte_short_dic(encrypt_func, _one_byte_short, offset_block, pre_pad_len)
        #print len(one_byte_short), one_byte_short
        cipher = encrypt_func(one_byte_short)
        #print len(cipher)
        #print cipher[: block_cnt*block_len]
        #print (block_cnt-1)*block_len, block_cnt*block_len
        cipher_block = cipher[(offset_block+block_cnt-1)*block_len : (offset_block+block_cnt)*block_len]
        c = dic[cipher_block]
        one_byte_short = one_byte_short[1:]
        r += c
        #print 'r=', r
    return r

def main():

    dcrpt_sfx = byte_at_a_time_ecb_decryption2(encrypt_with_fixed_key)
    #print dcrpt_sfx, len(dcrpt_sfx)
    #print suffix_str, len(suffix_str)
    if dcrpt_sfx == suffix_str:
        print "succeed:"
        print dcrpt_sfx
    else:
        print "failed"

if __name__ == "__main__":
    main()
