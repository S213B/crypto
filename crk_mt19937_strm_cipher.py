import mt19937
import my_rand
import base64
import time
#import crack_mt19937_seed

def prng_mode(prng_seed, prng_rand, seed, plain):
    cipher = ''
    prng_seed(seed)
    for i in range(len(plain)):
        rand_num = int(prng_rand() * 256)
        cipher += chr(ord(plain[i]) ^ rand_num)
    return cipher

def prng_encrypt(prng_seed, prng_rand, seed, plain):
    return prng_mode(prng_seed, prng_rand, seed, plain)

def prng_decrypt(prng_seed, prng_rand, seed, cipher):
    return prng_mode(prng_seed, prng_rand, seed, cipher)

time_stamp = None
orig_token = None
def gen_pswd_ret_token(l = 16):
    global orig_token, time_stamp
    token = ''
    cur_time = int(time.time())
    mt19937.seed_mt(cur_time)
    time_stamp = cur_time
    for i in range(l):
        token += chr(int(mt19937.random() * 256))
    token = base64.b64encode(token)
    orig_token = token
    return token

def valid_token(token):
    global orig_token, time_stamp
    cur_time = int(time.time())
    expire_time = 0
    if orig_token == token:
        expire_time += time_stamp
        orig_token = None
        time_stamp = None
        if expire_time < cur_time:
            #print "token valid"
            return True
        else:
            print "token expired"
            return False
    else:
        #print "token invalid"
        return False

def bf_crack_seed(cipher, knw_plain):
    for i in range(1 << 16):
        crk_plain = prng_decrypt(mt19937.seed_mt, mt19937.random, i, cipher)
        if crk_plain[-len(knw_plain):] == knw_plain:
            return i

def main():
    knw_plain = 'a' * 18
    plain = my_rand.my_rand_str(my_rand.my_rand(100, 10)) + knw_plain
    seed = my_rand.my_rand(1 << 16)
    print "plain length:", len(plain)

    cipher = prng_encrypt(mt19937.seed_mt, mt19937.random, seed, plain)
    crk_plain = prng_decrypt(mt19937.seed_mt, mt19937.random, seed, cipher)
    if plain == crk_plain:
        print "mt19937 stream cipher succeed"
    else:
        print "mt19937 stream cipher failed"

    #idx = len(cipher)-1
    #rand_num = ord(cipher[idx]) ^ ord('a')
    #crk_seed = crack_mt19937_seed.crack_mt19937_seed(rand_num, idx, 0, 1 << 16, lambda x : x % 256)
    crk_seed = bf_crack_seed(cipher, knw_plain)
    if seed == crk_seed:
        print "crack seed succeed", crk_seed
    else:
        print "crack seed failed, orig_seed:", seed, "crk_seed:", crk_seed

    token = gen_pswd_ret_token()
    if valid_token(token):
        print "token valid"
    else:
        print "toekn invalid"

if __name__ == "__main__":
    main()
