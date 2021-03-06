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

def get_offset(cipher, target):
    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, cbc_iv, cipher, aes_key)
    return plain.find(target)

def get_plain(cipher, s, e):
    plain = cbc_mode.cbc_decrypt(aes_128.aes_128_decrypt, cbc_iv, cipher, aes_key)
    return plain[s:e]

def main():
    plain = "12345678ladfnv01234567=+;890;admin=trueadjf+= ;adf"
    target = "admin"
    target2 = "=true;"
    cipher = encode(plain)
    offset = get_offset(cipher, target) - 1
    if offset == -2:
        print "cannot find target string in plain text, maybe encode"
        return

    cipher = cbc_bitflip_byte(cipher, get_plain(cipher, offset, offset+1), ';', offset)
    offset += len(target) + 1
    cipher = cbc_bitflip_str(cipher, get_plain(cipher, offset, offset+len(target2)), target2, offset)
    #cipher = cbc_bitflip_byte(cipher, '%', '=', offset + 6)
    #cipher = cbc_bitflip_byte(cipher, '3', 't', offset + 7)
    #cipher = cbc_bitflip_byte(cipher, 'd', 'r', offset + 8)
    #cipher = cbc_bitflip_byte(cipher, 't', 'u', offset + 9)
    #cipher = cbc_bitflip_byte(cipher, 'r', 'e', offset + 10)
    #cipher = cbc_bitflip_byte(cipher, 'u', ';', offset + 11)
    #print len(cipher)

    if is_admin(cipher):
        print "Is admin"
        #print get_plain(cipher, 0, len(cipher))
    else:
        print "Not admin"

if __name__ == "__main__":
    main()
