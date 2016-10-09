import ecb_mode
import struct

# ref:
# https://tools.ietf.org/html/rfc1320

a = None
b = None
c = None
d = None

def add(x, y):
    return (x+y) & 0xFFFFFFFF #% (1<<32)

def rotl(x, n):
    #if (x >> (32-n)) != ((x & 0xFFFFFFFF) >> (32-n)):
    #    print format(x, "016X"), 32-n
    #    print format(x >> (32-n), "016X")
    #    print format((x & 0xFFFFFFFF) >> (32-n), "016X")
    #    print

    # x & 0xFFFFFFFF is fragile
    return ((x << n) | ((x & 0xFFFFFFFF) >> (32-n))) & 0xFFFFFFFF

def f(x, y, z):
    return ((x & y) | ((~(x)) & z)) & 0xFFFFFFFF

def g(x, y, z):
    return ((x & y) | (x & z) | (y & z)) & 0xFFFFFFFF

def h(x, y, z):
    return (x ^ y ^ z) & 0xFFFFFFFF

def padding(msg):
    pad_str = chr(0x80)
    len_str = struct.pack('<Q', len(msg)*8)
    zero_pad_len = (((~(len(msg) + 9)) & (64-1)) + 1) & (64-1)
    zero_str = chr(0) * zero_pad_len
    pad_str += zero_str + len_str
    return pad_str

def parsing(msg):
    return ecb_mode.text_to_blocks(msg, 64)

def init_hash_val(h0 = 0x67452301, h1 = 0xefcdab89, h2 = 0x98badcfe, h3 = 0x10325476):
    global a, b, c, d
    a = h0
    b = h1
    c = h2
    d = h3

def preproc(msg):
    init_hash_val()
    msg += padding(msg)
    #print len(msg)
    msg = parsing(msg)
    return msg

def gen_msg_schdl(blk):
    x = []
    blk = ecb_mode.text_to_blocks(blk, 4)
    for b in blk:
        x += struct.unpack("<I", b)
    return x

def ff(a, b, c, d, x_k, s):
    return rotl(a + f(b, c, d) + x_k, s)

def gg(a, b, c, d, x_k, s):
    return rotl(a + g(b, c, d) + x_k + 0x5A827999, s)

def hh(a, b, c, d, x_k, s):
    return rotl(a + h(b, c, d) + x_k + 0x6ED9EBA1, s)

def compute(blks):
    global a, b, c, d
    for blk in blks:
        x = gen_msg_schdl(blk)
        aa = a
        bb = b
        cc = c
        dd = d

        a = ff(a, b, c, d, x[ 0],  3)
        d = ff(d, a, b, c, x[ 1],  7)
        c = ff(c, d, a, b, x[ 2], 11)
        b = ff(b, c, d, a, x[ 3], 19)
        a = ff(a, b, c, d, x[ 4],  3)
        d = ff(d, a, b, c, x[ 5],  7)
        c = ff(c, d, a, b, x[ 6], 11)
        b = ff(b, c, d, a, x[ 7], 19)
        a = ff(a, b, c, d, x[ 8],  3)
        d = ff(d, a, b, c, x[ 9],  7)
        c = ff(c, d, a, b, x[10], 11)
        b = ff(b, c, d, a, x[11], 19)
        a = ff(a, b, c, d, x[12],  3)
        d = ff(d, a, b, c, x[13],  7)
        c = ff(c, d, a, b, x[14], 11)
        b = ff(b, c, d, a, x[15], 19)

        a = gg(a, b, c, d, x[ 0],  3)
        d = gg(d, a, b, c, x[ 4],  5)
        c = gg(c, d, a, b, x[ 8],  9)
        b = gg(b, c, d, a, x[12], 13)
        a = gg(a, b, c, d, x[ 1],  3)
        d = gg(d, a, b, c, x[ 5],  5)
        c = gg(c, d, a, b, x[ 9],  9)
        b = gg(b, c, d, a, x[13], 13)
        a = gg(a, b, c, d, x[ 2],  3)
        d = gg(d, a, b, c, x[ 6],  5)
        c = gg(c, d, a, b, x[10],  9)
        b = gg(b, c, d, a, x[14], 13)
        a = gg(a, b, c, d, x[ 3],  3)
        d = gg(d, a, b, c, x[ 7],  5)
        c = gg(c, d, a, b, x[11],  9)
        b = gg(b, c, d, a, x[15], 13)
        
        a = hh(a, b, c, d, x[ 0],  3)
        d = hh(d, a, b, c, x[ 8],  9)
        c = hh(c, d, a, b, x[ 4], 11)
        b = hh(b, c, d, a, x[12], 15)
        a = hh(a, b, c, d, x[ 2],  3)
        d = hh(d, a, b, c, x[10],  9)
        c = hh(c, d, a, b, x[ 6], 11)
        b = hh(b, c, d, a, x[14], 15)
        a = hh(a, b, c, d, x[ 1],  3)
        d = hh(d, a, b, c, x[ 9],  9)
        c = hh(c, d, a, b, x[ 5], 11)
        b = hh(b, c, d, a, x[13], 15)
        a = hh(a, b, c, d, x[ 3],  3)
        d = hh(d, a, b, c, x[11],  9)
        c = hh(c, d, a, b, x[ 7], 11)
        b = hh(b, c, d, a, x[15], 15)

        a = add(a, aa)
        b = add(b, bb)
        c = add(c, cc)
        d = add(d, dd)

    h = struct.pack("<I", a)
    h += struct.pack("<I", b)
    h += struct.pack("<I", c)
    h += struct.pack("<I", d)

    return h

def md4(msg):
    blks = preproc(msg)
    h = compute(blks)
    return h

def hmac_md4(key, msg):
    return md4(key + msg)

def main():
    import binascii
    assert binascii.hexlify(md4('')) == "31d6cfe0d16ae931b73c59d7e0c089c0"
    assert binascii.hexlify(md4('a')) == "bde52cb31de33e46245e05fbdbd6fb24"
    assert binascii.hexlify(md4("abc")) == "a448017aaf21d8525fc10ae87aa6729d"
    assert binascii.hexlify(md4("message digest")) == "d9130a8164549fe818874806e1c7014b"
    assert binascii.hexlify(md4("abcdefghijklmnopqrstuvwxyz")) == "d79e1c308aa5bbcdeea8ed63df412da9"
    assert binascii.hexlify(md4("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")) == "043f8582f241db351ce627e153e7f0e4"
    assert binascii.hexlify(md4("12345678901234567890123456789012345678901234567890123456789012345678901234567890")) == "e33b4ddc9c38f2199c3e7b164fcc0536"

if __name__ == "__main__":
    main()
