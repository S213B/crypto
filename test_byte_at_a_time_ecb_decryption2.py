import os
import byte_at_a_time_ecb_decryption2
import byte_at_a_time_ecb_decryption

print byte_at_a_time_ecb_decryption2.byte_at_a_time_ecb_decryption2(byte_at_a_time_ecb_decryption.encrypt_with_fixed_key)

for x in range(30):
    os.system("python byte_at_a_time_ecb_decryption2.py")
