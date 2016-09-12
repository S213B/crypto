import time

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

def seed_mt(seed):
    global idx, MT
    idx = n
    MT[0] = seed
    for i in range(1, len(MT)):
        MT[i] = (f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i) & (lower_mask | upper_mask)

def extract_number():
    global idx, MT
    if idx is None:
        seed_mt(int(time.time() + 213))
        idx = n
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

def random():
    return extract_number()
    #return extract_number() / float(lower_mask | upper_mask)

seed_mt(int(time.time() + 213))
#seed_mt(213)

def main():
    for i in range(10):
        print random()

if __name__ == "__main__":
    main()
