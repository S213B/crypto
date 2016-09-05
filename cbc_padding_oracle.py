import pkcs7
import cbc_mode
import aes_128
import my_rand
import binascii
import ecb_mode
import xor_encrypt

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
    import base64
    plain = base64.b64decode(plain)
    global test_plain
    test_plain = plain
    iv = my_rand.my_rand_byte(16)
    iv_str = ''.join([chr(i) for i in iv])
    cipher = cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, iv, plain, aes_key)
    #token = iv_str + cipher
    return iv_str, cipher
    #return binascii.hexlify(iv_str), binascii.hexlify(cipher)

def valid_token(iv, cipher):
    #iv = binascii.unhexlify(iv)
    iv = [ord(i) for i in iv]
    #cipher = binascii.unhexlify(cipher)
    return cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, iv, cipher, aes_key)

def cbc_padding_oracle_core(valid_func, block):
    plain = ''
    block_size = len(block)
    for i in reversed(range(block_size)):
        for j in range(256):
            pad_val = block_size - i
            iv = 'a' * i + chr(pad_val ^ j) + ''.join([chr(ord(c) ^ pad_val) for c in plain])
            try:
                valid_func(iv, block)
                plain = chr(j) + plain
                break
            except Exception:
                pass
    return plain

def cbc_padding_oracle(valid_func, iv, cipher):
    # preassume add_func in cbc_mode is xor
    plain = ''
    block_size = len(iv)
    blocks = ecb_mode.text_to_blocks(cipher, block_size)
    for i in range(len(blocks)):
        block = blocks[i]
        tmp_plain = cbc_padding_oracle_core(valid_func, block)
        plain += xor_encrypt.xor_encrypt_str(iv, tmp_plain)
        iv = block
    return plain

def diff(orig, new):
    if len(orig) == len(new):
        for i in range(len(orig)):
            if orig[i] != new[i]:
                print "idx:", i, "orig:", orig[i], "new:", new[i]
    else:
        print "orig length:", len(orig)
        print "new length:", len(new)

def main():
    iv, cipher = gen_token()
    #print iv, cipher
    
    plain = valid_token(iv, cipher)
    if plain == test_plain:
        print "validate token succeed"
        #print test_plain
        #print plain
    else:
        print "validate token failed"
        diff(test_plain, plain)

    plain = cbc_padding_oracle(valid_token, iv, cipher)
    plain = pkcs7.pkcs7_unpad(plain, len(iv))
    if plain == test_plain:
        print "CBC padding oracle succeed"
        #print test_plain
        print plain
    else:
        print "CBC padding oracle failed"
        diff(test_plain, plain)

if __name__ == "__main__":
    main()
