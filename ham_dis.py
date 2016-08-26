def cnt1(c):
    r = 0
    while c != 0:
        r += c & 1
        c = c >> 1
    return r

def ham_dis(s1, s2):
    if len(s1) != len(s2):
        print 'input strings are not equal in length'
        return None

    cnt = 0

    for idx in range(len(s1)):
        cnt += cnt1(ord(s1[idx]) ^ ord(s2[idx]))

    return cnt

if __name__ == '__main__':
    s1 = 'this is a test'
    s2 = 'wokka wokka!!!'
    print ham_dis(s1, s2)
