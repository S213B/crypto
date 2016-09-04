import pkcs7
import cbc_mode
import aes_128
import my_rand
import binascii

aes_key = my_rand.my_rand_str(16)
token_plain = [
"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]
test_plain = None

def gen_token():
    plain = token_plain[my_rand.my_rand(len(token_plain))]
    global test_plain
    test_plain = plain
    iv = my_rand.my_rand_byte(16)
    iv_str = ''.join([chr(i) for i in iv])
    cipher = cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, iv, plain, aes_key)
    token = iv_str + cipher
    #return iv, cipher
    return binascii.hexlify(iv_str), binascii.hexlify(cipher)

def valid_token(iv, cipher):
    iv = binascii.unhexlify(iv)
    iv = [ord(i) for i in iv]
    cipher = binascii.unhexlify(cipher)
    return cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, iv, cipher, aes_key)

def main():
    iv, cipher = gen_token()
    #print iv, cipher
    
    plain = valid_token(iv, cipher)
    if plain != test_plain:
        print "Error"
    #    for i in range(len(plain)):
    #        if plain[i] != test_plain[i]:
    #            print i, plain[i]

if __name__ == "__main__":
    main()
