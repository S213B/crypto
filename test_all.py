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
"ctr_mode.py",
"brk_fixed_iv_ctr.py",
"brk_fixed_iv_ctr2.py",
"mt19937.py",
"crack_mt19937_seed.py",
"clone_mt19937_rng.py",
"crk_mt19937_strm_cipher.py",
"crk_rarw_aes_ctr.py",
"ctr_bitflip_atk.py",
"crk_cbc_iv_eq_key.py",
"sha1.py",
"brk_hmac_by_len_ext.py",
"md4.py",
"brk_hmac_by_len_ext2.py",
]

for f in files:
    #print f + ':'
    cmd = "python " + f
    os.system(cmd)
    #print
