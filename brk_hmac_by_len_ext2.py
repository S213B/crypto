import md4
import my_rand
import struct

hmac_key = my_rand.my_rand_str(my_rand.my_rand(213, 8))

def auth(msg):
    global hmac_key
    return md4.hmac_md4(hmac_key, msg)

def verify(msg, hmac):
    global hmac_key
    return md4.hmac_md4(hmac_key, msg) == hmac

def cal_md4_padding(msg):
    return md4.padding(msg)

def md4_with_init(msg, h0, h1, h2, h3):
    md4.init_hash_val(h0, h1, h2, h3)
    #msg += md4.padding(msg)
    blks = md4.parsing(msg)
    h = md4.compute(blks)
    return h

def len_ext_atk2(ori_msg, new_msg, ori_hmac, verify_func = verify):
    h0 = struct.unpack("<I", ori_hmac[0:4])[0]
    h1 = struct.unpack("<I", ori_hmac[4:8])[0]
    h2 = struct.unpack("<I", ori_hmac[8:12])[0]
    h3 = struct.unpack("<I", ori_hmac[12:16])[0]
    for i in range(5000):
        asum_key = 'a' * i
        glue_pad = cal_md4_padding(asum_key + ori_msg)
        msg = ori_msg + glue_pad + new_msg
        new_pad = cal_md4_padding(asum_key + msg)
        hmac = md4_with_init(new_msg + new_pad, h0, h1, h2, h3)
        if verify_func(msg, hmac):
            return msg, hmac
    return None, None

def main():
    msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    hmac = auth(msg)
    if verify(msg, hmac):
        print "verification succeed"
    else:
        print "verification failed"

    apd_msg = ";admin=true"
    new_msg, new_hmac = len_ext_atk2(msg, apd_msg, hmac)
    if new_msg is not None:
        print "length extension attack succeed"
        import binascii
        print new_msg
        #print binascii.hexlify(new_msg)
        print binascii.hexlify(new_hmac)
    else:
        print "length extension attack failed"

if __name__ == "__main__":
    main()
