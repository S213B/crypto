import random

class DiffieHellman:
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2

    def __init__(self, p = None, g = None):
        if p is not None:
            self.p = p
        if g is not None:
            self.g = g
        return

    def gen_pri_key(self):
        return random.getrandbits(200) % self.p

    def gen_pub_key(self, pri_key):
        pub_key = pow(self.g, pri_key, self.p)
        return pub_key, self.p, self.g

    def gen_key_pair(self):
        pri_key = self.gen_pri_key()
        pub_key, p, g = self.gen_pub_key(pri_key)
        return pri_key, pub_key, p, g

    def gen_sec_key(self, peer_pub_key, self_pri_key):
        return pow(peer_pub_key, self_pri_key, self.p)

def main():
    a_dh = DiffieHellman()
    a_pri, a_pub, a_p, a_g = a_dh.gen_key_pair()

    b_dh = DiffieHellman(a_p, a_g)
    b_pri, b_pub, b_p, b_g = b_dh.gen_key_pair()

    a_sk = a_dh.gen_sec_key(b_pub, a_pri)
    b_sk = b_dh.gen_sec_key(a_pub, b_pri)

    if a_sk != b_sk:
        print "generating secret key failed"
        print "Alice generate secret key", a_sk
        print "Bob generate secret key", b_sk
    else:
        print "generating secret key succeed"

if __name__ == "__main__":
    main()
