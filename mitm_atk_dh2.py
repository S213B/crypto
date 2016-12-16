from diffie_hellman import DiffieHellman
import sha1
import binascii

#Cannot understand the question

def main():
    #replace g with 1, p, p-1...
    #just watch the generated secret key result
    #1  : all secret keys are 1
    #p  : all secret keys are 0
    #p-1: half secret keys are 1
    #     half secret keys are p-1
    dh = DiffieHellman(DiffieHellman.p, 1)
    a_pri, a_pub, a_p, a_g = dh.gen_key_pair()
    b_pri, b_pub, b_p, b_g = dh.gen_key_pair()
    a_sk = dh.gen_sec_key(b_pub, a_pri)
    key_a = sha1.sha1(str(a_sk))[:16]
    print a_sk
    print binascii.hexlify(key_a)

    dh = DiffieHellman(DiffieHellman.p, DiffieHellman.p)
    a_pri, a_pub, a_p, a_g = dh.gen_key_pair()
    b_pri, b_pub, b_p, b_g = dh.gen_key_pair()
    a_sk = dh.gen_sec_key(b_pub, a_pri)
    key_a = sha1.sha1(str(a_sk))[:16]
    print a_sk
    print binascii.hexlify(key_a)

    dh = DiffieHellman(DiffieHellman.p, DiffieHellman.p-1)
    a_pri, a_pub, a_p, a_g = dh.gen_key_pair()
    b_pri, b_pub, b_p, b_g = dh.gen_key_pair()
    a_sk = dh.gen_sec_key(b_pub, a_pri)
    key_a = sha1.sha1(str(a_sk))[:16]
    print a_sk
    print binascii.hexlify(key_a)
    
if __name__ == "__main__":
    for i in range(100):
        main()
