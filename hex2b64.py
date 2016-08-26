import base64
import binascii

def hex2b64(in_str):
    t_str = binascii.unhexlify(in_str)
    return base64.b64encode(t_str)

if __name__ == '__main__':
    str = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print hex2b64(str)
