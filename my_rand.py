import random
import string

# [start, end)
def my_rand(end, start = 0):
    num = int(random.random() * (end - start))
    return num + start

def my_rand_str(len):
    r = ''
    for i in range(len):
        while True:
            c = chr(my_rand(128))
            if c in string.printable:
                r += c
                break
    return r

def my_rand_byte(len):
    r = []
    for i in range(len):
        c = my_rand(256)
        r.append(c)
    return r

'''
def my_rand_aes_key(len):
    if len == 128:
        return my_rand_str(16)
    elif len == 192:
        return my_rand_str(24)
    elif len == 256:
        return my_rand_str(32)
    else:
        return None
'''
