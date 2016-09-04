import cbc_mode
import aes_128
import my_rand

aes_key = my_rand.my_rand_str(16)
cbc_iv = my_rand.my_rand_byte(16)

def encode_str(plain):
    percent = '%%%x' % ord('%')
    semicolon = '%%%x' % ord(';')
    equality = '%%%x' % ord('=')
    space = '%%%x' % ord(' ')
    plain = plain.replace('%', percent)
    plain = plain.replace(';', semicolon)
    plain = plain.replace('=', equality)
    plain = plain.replace(' ', space)
    cipher = plain
    return cipher

def encode(user_data):
    pre_str = "comment1=cooking%20MCs;userdata=";
    app_str = ";comment2=%20like%20a%20pound%20of%20bacon";

    plain = pre_str + encode_str(user_data) + app_str;

    return cbc_mode.cbc_encrypt(aes_128.aes_128_encrypt, cbc_iv, plain, aes_key)

def is_admin(cipher):
    target = ";admin=true;"

    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, cbc_iv, cipher, aes_key)
    #print len(plain)
    #print plain

    return target in plain

def bitflip(orig_ch, fr, to):
    flip = ord(fr) ^ ord(to)
    orig_byte = ord(orig_ch)
    return chr(orig_byte ^ flip)

def cbc_bitflip_byte(cipher, fr, to, offset, block_size = 16):
    offset -= block_size
    return cipher[:offset] + bitflip(cipher[offset], fr, to) + cipher[offset+1:]

def cbc_bitflip_str(cipher, fr, to, offset, block_size = 16):
    if len(fr) != len(to):
        print "from & to are not in equal length"
    for i in range(len(fr)):
        cipher = cbc_bitflip_byte(cipher, fr[i], to[i], offset + i, block_size)
    return cipher

def main():
    plain = "123456789012345678901234567890;admin=true"
    cipher = encode(plain)
    offset = 64     # calculate depend on the decoded cipher text
    jump = len("admin") + 1
    cipher = cbc_bitflip_byte(cipher, 'b', ';', offset)
    cipher = cbc_bitflip_str(cipher, "%3dtru", "=true;", offset + jump)
    #cipher = cbc_bitflip_byte(cipher, '%', '=', offset + 6)
    #cipher = cbc_bitflip_byte(cipher, '3', 't', offset + 7)
    #cipher = cbc_bitflip_byte(cipher, 'd', 'r', offset + 8)
    #cipher = cbc_bitflip_byte(cipher, 't', 'u', offset + 9)
    #cipher = cbc_bitflip_byte(cipher, 'r', 'e', offset + 10)
    #cipher = cbc_bitflip_byte(cipher, 'u', ';', offset + 11)
    #print len(cipher)
    if is_admin(cipher):
        print "Is admin"
    else:
        print "Not admin"

if __name__ == "__main__":
    main()
