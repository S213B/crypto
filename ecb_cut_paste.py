from my_rand import *
from aes_128 import *
from ecb_mode import ecb_encrypt, ecb_decrypt

def is_email_valid(email):
    if '#' in email or '=' in email:
        print "'#' and '=' are not allowed in email address"
        return False
    else:
        return True

def cookie_2_dic(cookie):
    r = {}
    for part in cookie.split('&'):
        if len(part.split('=')) != 2:
            print "cookie syntax error"
            return None
        key, value = part.split('=')
        r[key] = value
    return r

def dic_2_cookie(dic):
    cookie = ''
    for key in dic:
        value = dic[key]
        if '&' in key or '=' in key or '&' in value or '=' in value:
            print "'#' and '=' are not allowed in key or value of cookie"
            return None
        cookie += key + '=' + value + '&'
    return cookie[:-1]

def add_dic_itm(dic, key, value):
    if '&' in key or '=' in key:
        print "'#' and '=' are not allowed in key"
        return None
    if '&' in value or '=' in value:
        print "'#' and '=' are not allowed in value"
        return None
    dic[key] = value
    return dic

def get_role(is_admin):
    if is_admin:
        return "admin"
    else:
        return "user"

def profile_for(email, is_admin = False):
    if not is_email_valid(email):
        return None
    dic = {}
    if not add_dic_itm(dic, "email", email):
        return None
    if not add_dic_itm(dic, "uid", str(my_rand(213))):
        return None
    if not add_dic_itm(dic, "role", get_role(is_admin)):
        return None
    return dic

def my_encode(dic):
    return dic_2_cookie(dic)

def my_decode(cookie):
    return cookie_2_dic(cookie)

def main():
    key = my_rand_str(16)

    plain_dic = profile_for("xlq.s213b@gmail.com")
    plain_cookie = my_encode(plain_dic)
    plain = plain_cookie
    print "plain:\n" + plain

    cipher = ecb_encrypt(aes_128_encrypt, plain, key)

    plain = ecb_decrypt(aes_128_decrypt, cipher, key)

    plain_cookie = plain
    plain_dic = my_decode(plain_cookie)
    print "plain:\n" + plain

if __name__ == "__main__":
    main()
