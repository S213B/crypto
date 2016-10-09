import my_rand
import mt19937
import time

def foo():
    t = my_rand.my_rand(10, 1)
    #t = my_rand.my_rand(1000, 10)
    time.sleep(t)

    seed = int(time.time())
    #print "seed:", seed
    mt19937.seed_mt(seed)

    t = my_rand.my_rand(10, 1)
    #t = my_rand.my_rand(1000, 10)
    time.sleep(t)

    return mt19937.extract_number(), seed

def make_mt19937_rand_list(idx, rng_s, rng_e):
    if rng_s > rng_e:
        rng_s, rng_e = rng_e, rng_s
    rand_list = {}
    for i in range(rng_s, rng_e):
        mt19937.seed_mt(i)
        for j in range(idx):
            mt19937.extract_number()
        rand_num = mt19937.extract_number()
        rand_list[rand_num] = i
    return rand_list

def crack_mt19937_seed(rand_num, idx, rng_s, rng_e):
    rand_list = make_mt19937_rand_list(idx, rng_s, rng_e)
    if rand_num in rand_list:
        return rand_list[rand_num]
    else:
        return None

def main():
    rand_num, seed = foo()
    rng = int(time.time())
    crack_seed = crack_mt19937_seed(rand_num, 0, rng-2000, rng)
    if crack_seed == seed:
        print "crack succeed:", crack_seed
    else:
        print "crack failed"

if __name__ == "__main__":
    main()
