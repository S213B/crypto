import my_rand
import mt19937
import time

def crack_mt19937_seed():
    time.sleep(my_rand.my_rand(1000, 40))
    mt19937.seed_mt(int(time.time()))
    time.sleep(my_rand.my_rand(1000, 40))
    return mt19937.random()

def main():
    #for i in range(10):
    print crack_mt19937_seed()

if __name__ == "__main__":
    main()
