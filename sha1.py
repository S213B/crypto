import ecb_mode
import struct

# ref:
# http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
# https://tools.ietf.org/html/rfc3174

h0 = None
h1 = None
h2 = None
h3 = None
h4 = None

def add(x, y):
    return (x+y) & 0xFFFFFFFF #% (1<<32)

def rotl(x, n):
    return ((x << n) | (x >> (32-n))) & 0xFFFFFFFF

def ch(x, y, z):
    return (x & y) ^ ((~x) & 0xFFFFFFFF & z)

def parity(x, y, z):
    return x ^ y ^ z

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def foo(x, y, z, t):
    if 0 <= t and t <= 19:
        return ch(x, y, z)
    if 20 <= t and t <= 39:
        return parity(x, y, z)
    if 40 <= t and t <= 59:
        return maj(x, y, z)
    if 60 <= t and t <= 79:
        return parity(x, y, z)

def get_const(t):
    #   [0, 19],    [20, 39],   [40, 59],   [60, 79]
    k = [0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xca62c1d6]
    return k[t/20]

def padding(msg):
    pad_str = chr(0x80)
    len_str = struct.pack('>Q', len(msg)*8)
    zero_pad_len = (((~(len(msg) + 9)) & (64-1)) + 1) & (64-1)
    zero_str = chr(0) * zero_pad_len
    pad_str += zero_str + len_str
    return pad_str

def parsing(msg):
    return ecb_mode.text_to_blocks(msg, 64)

def init_hash_val(a = 0x67452301, b = 0xefcdab89, c = 0x98badcfe, d = 0x10325476, e = 0xc3d2e1f0):
    global h0, h1, h2, h3, h4
    h0 = a
    h1 = b
    h2 = c
    h3 = d
    h4 = e

def preproc(msg):
    init_hash_val()
    msg += padding(msg)
    #print len(msg)
    msg = parsing(msg)
    return msg

def gen_msg_schdl(blk):
    w = []
    blk = ecb_mode.text_to_blocks(blk, 4)
    for i in range(80):
        if i <= 15:
            w += struct.unpack(">I", blk[i])
        else:
            t = rotl(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
            w.append(t)
    return w

def compute(blks):
    global h0, h1, h2, h3, h4
    for blk in blks:
        w = gen_msg_schdl(blk)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        for t in range(80):
            T = add(rotl(a, 5), foo(b, c, d, t))
            T = add(T, e)
            T = add(T, get_const(t))
            T = add(T, w[t])
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = T
        h0 = add(a, h0)
        h1 = add(b, h1)
        h2 = add(c, h2)
        h3 = add(d, h3)
        h4 = add(e, h4)
    h = struct.pack(">I", h0)
    h += struct.pack(">I", h1)
    h += struct.pack(">I", h2)
    h += struct.pack(">I", h3)
    h += struct.pack(">I", h4)
    return h

# msg : str
# h   : str
def sha1(msg):
    blks = preproc(msg)
    h = compute(blks)
    return h

# key : str
# informal implementation, do not use
# use hmac_sha1() inside hmac.py instead
def hmac_sha1(key, msg):
    return sha1(key + msg)

def main():
    import my_rand
    import sha
    import binascii
    for i in range(213):
        msg = my_rand.my_rand_str(my_rand.my_rand(213))
        h = sha1(msg)
        s = sha.new(msg)
        if h != s.digest():
            print "SHA-1 failed"
            print len(msg)
            print h
            print s.digest()

    key = "This is key"
    msg = my_rand.my_rand_str(my_rand.my_rand(213))
    hmac = hmac_sha1(key, msg)
    print binascii.hexlify(hmac)

if __name__ == "__main__":
    main()
