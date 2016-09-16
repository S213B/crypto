import ctr_mode
import my_rand
import mt19937

aes_key = my_rand.my_rand_str(16)
ctr_iv = mt19937.extract_number()

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
    #print len(plain)
    #print plain

    return ctr_mode.ctr_encrypt(aes_key, ctr_iv, plain)

def is_admin(cipher):
    target = ";admin=true;"

    plain = ctr_mode.ctr_decrypt(aes_key, ctr_iv, cipher)
    #print len(plain)
    #print plain

    return target in plain

def bitflip(orig_ch, fr, to):
    flip = ord(fr) ^ ord(to)
    orig_byte = ord(orig_ch)
    return chr(orig_byte ^ flip)

def ctr_bitflip_byte(cipher, fr, to, offset):#, block_size = 16):
    #offset -= block_size
    return cipher[:offset] + bitflip(cipher[offset], fr, to) + cipher[offset+1:]

def ctr_bitflip_str(cipher, fr, to, offset):#, block_size = 16):
    if len(fr) != len(to):
        print "from & to are not in equal length"
    for i in range(len(fr)):
        cipher = ctr_bitflip_byte(cipher, fr[i], to[i], offset + i)#, block_size)
    return cipher

def get_offset(cipher, target):
    plain = ctr_mode.ctr_decrypt(aes_key, ctr_iv, cipher)
    return plain.find(target)

def get_plain(cipher, s, e):
    plain = ctr_mode.ctr_decrypt(aes_key, ctr_iv, cipher)
    return plain[s:e]

def main():
    plain = "126=78901230123456;admin=true0123;=; sda"
    target = "admin"
    target2 = "=true;"
    cipher = encode(plain)
    offset = get_offset(cipher, target) - 1
    if offset == -2:
        print "cannot find target string in plain text, maybe encode"
        return

    cipher = ctr_bitflip_byte(cipher, get_plain(cipher, offset, offset+1), ';', offset)
    offset += len(target) + 1
    cipher = ctr_bitflip_str(cipher, get_plain(cipher, offset, offset+len(target2)), target2, offset)
    #print len(cipher)

    if is_admin(cipher):
        print "Is admin"
        #print get_plain(cipher, 0, len(cipher))
    else:
        print "Not admin"

if __name__ == "__main__":
    main()
