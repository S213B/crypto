import sha1
import xor_encrypt

# ref
# https://tools.ietf.org/html/rfc2104

def hmac_sha1(key, msg):
    blk_sz = 64
    len_opt = 20
    ipad = chr(0x36) * blk_sz
    opad = chr(0x5C) * blk_sz
    if len(key) > blk_sz:
        key = sha1.sha1(key)
    key += chr(0) * (blk_sz - len(key))

    sub_msg = xor_encrypt.xor_encrypt_str(key, ipad)
    sub_msg = sha1.sha1(sub_msg + msg)
    msg = xor_encrypt.xor_encrypt_str(key, opad) + sub_msg
    return sha1.sha1(msg)

def main():
    import binascii
    assert binascii.hexlify(hmac_sha1("213", "111111")) == "1fb5b9c090d6ba0df9858a2aeded62c5e363bd0f"
    assert binascii.hexlify(hmac_sha1("213", "12345678hhljadsfn,ansdfoiwern,anxmcnvkadhfoweiu230rladsfakjsdhfkzbnakfhasdwor823rhjhadf")) == "c92315c6bfb2e8ea83d50680a09dda39032df70a"
    assert binascii.hexlify(hmac_sha1("213213213213213213213213", "123456")) == "ab9da692009f111734baa23dd37564ef666c14ab"
    assert binascii.hexlify(hmac_sha1("213213213213213213213213", "12345678hhljadsfn,ansdfoiwern,anxmcnvkadhfoweiu230rladsfakjsdhfkzbnakfhasdwor823rhjhadf")) == "be1ef203a0bebe55fc66c48030a153f21c71450c"
    assert binascii.hexlify(hmac_sha1("1234567890asdfghjklp", "zxcvbnm")) == "714e4989aaaaea7f07c47cf0388e36379e26269b"
    assert binascii.hexlify(hmac_sha1("1234567890asdfghjklp", "zxcvbnm1234567890q wertyuioplkjhgfdsa[;,o8vgnshfjvnavb lpasbd")) == "c78baac0f4e1f53fbaf652597f1997d6d4c51df4"

if __name__ == "__main__":
    main()
