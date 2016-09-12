import mt19937

w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
u, d = 11, 0xFFFFFFFF
s, b = 7, 0x9D2C5680
t, c = 15, 0xEFC60000
l = 18
f = 1812433253

MT = [None] * n
idx = None
lower_mask = (1 << r) - 1
upper_mask = ((w - r + 1) - 1) << r

def untemper(z):
    y = z ^ (z >> 18)
    #y_15 = y & 0x7FFF
    #y_30 = (y ^ ((y_15 << 15) & 0xEFC60000)) & 0x3FFF8000
    #y_32 = (y ^ ((y_30 << 15) & 0xEFC60000)) & 0xC0000000
    #y = y_32 | y_30 | y_15
    y = y ^ ((y << 15) & 0xEFC60000)
    y_7 = y & 0x7F
    y_14 = (y ^ ((y_7 << 7) & 0x9D2C5680)) & 0x3F80
    y_21 = (y ^ ((y_14 << 7) & 0x9D2C5680)) & 0x1FC000
    y_28 = (y ^ ((y_21 << 7) & 0x9D2C5680)) & 0xFE00000
    y_32 = (y ^ ((y_28 << 7) & 0x9D2C5680)) & 0xF0000000
    y = y_32 | y_28 | y_21 | y_14 | y_7
    x = y ^ (y >> 11) ^ (y >> 22)
    return x

def extract_number():
    global idx, MT
    if idx >= n:
        twist()
    x = MT[idx]
    y = x ^ ((x >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    z = y ^ (y >> l)
    idx += 1
    return z & (lower_mask | upper_mask)

def twist():
    global idx, MT
    for i in range(len(MT)):
        t = ((MT[i] & upper_mask) | (MT[(i+1) % n] & lower_mask))
        t >>= 1
        if t & 1 != 0:
            t ^= a
        MT[i] = MT[(i+m) % n] ^ t
    idx = 0

def clone_mt19937_rng():
    global n, idx, MT
    for i in range(n):
        MT[i] = untemper(mt19937.random())
    idx = n

def main():
    #for i in range(10):
    clone_mt19937_rng()
    for i in range(n * 3 + 213):
        orig = mt19937.random()
        clone = extract_number()
        #print "orig:", orig
        #print "clone:", clone
        if orig != clone:
            print "clone failed"
            return
    print "clone succeed"

if __name__ == "__main__":
    main()
