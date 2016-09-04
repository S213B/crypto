import os

files = [
"hex2b64.py",
"xor2str.py",
"single_byte_xor_cipher.py",
"detect_single_c_xor.py",
"xor_encrypt.py",
"rep_xor_decrypt.py",
"aes_128.py",
"ecb_detect.py",
"pkcs7.py",
"cbc_mode.py",
"ecb_cbc_detect.py",
"byte_at_a_time_ecb_decryption.py",
"ecb_cut_paste.py",
"byte_at_a_time_ecb_decryption2.py",
"pkcs7.py",
"cbc_bitflip_atk.py",
"cbc_padding_oracle.py",
]

for f in files:
    #print f + ':'
    cmd = "python " + f
    os.system(cmd)
    #print
