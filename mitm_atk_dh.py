import diffie_hellman
import sha1
import my_rand
import cbc_mode
import aes_128

def main():
    dh = diffie_hellman.DiffieHellman()

    a_pri, a_pub, a_p, a_g = dh.gen_key_pair()
    m_pri, m_pub, m_p, m_g = dh.gen_key_pair()
    b_pri, b_pub, b_p, b_g = dh.gen_key_pair()

    a_sk = dh.gen_sec_key(m_pub, a_pri)
    key_a = sha1.sha1(str(a_sk))[:16]
    iv_a = my_rand.my_rand_byte(16)

    b_sk = dh.gen_sec_key(m_pub, b_pri)
    key_b = sha1.sha1(str(b_sk))[:16]
    iv_b = my_rand.my_rand_byte(16)

    plain_ori = my_rand.my_rand_str(my_rand.my_rand(30, 10))

    print "Sending following text from A to B..."
    print "\t" + plain_ori
    cipher = cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, iv_a, plain_ori, key_a)

    print "Text intercepted by M is:"
    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, iv_a, cipher, key_a)
    print "\t" + plain

    print "Forwarding text from M to B..."
    cipher = cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, iv_b, plain, key_b)

    print "Text received by B is:"
    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, iv_b, cipher, key_b)
    print "\t" + plain

    if plain == plain_ori:
        print "OK"
    else:
        print "Fail"
    
if __name__ == "__main__":
    main()
