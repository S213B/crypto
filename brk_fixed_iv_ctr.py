import ctr_mode
import my_rand
import base64
import string
import xor_encrypt
import sys

plains = [
        "SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==",
        "Q29taW5nIHdpdGggdml2aWQgZmFjZXM=",
        "RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==",
        "RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=",
        "SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk",
        "T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=",
        "UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
        "QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=",
        "T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl",
        "VG8gcGxlYXNlIGEgY29tcGFuaW9u",
        "QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==",
        "QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=",
        "QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==",
        "QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
        "VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==",
        "SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==",
        "SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==",
        "VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==",
        "V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==",
        "V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==",
        "U2hlIHJvZGUgdG8gaGFycmllcnM/",
        "VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=",
        "QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=",
        "VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=",
        "V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=",
        "SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==",
        "U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==",
        "U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=",
        "VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==",
        "QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu",
        "SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=",
        "VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs",
        "WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=",
        "SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0",
        "SW4gdGhlIGNhc3VhbCBjb21lZHk7",
        "SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=",
        "VHJhbnNmb3JtZWQgdXR0ZXJseTo=",
        "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
        ]

def string_valid(s):
    #str_valid = string.ascii_lowercase + string.ascii_uppercase + "',.!? -"
    str_valid = string.printable
    for c in s:
        if c not in str_valid:
            return False
    return True

def cal_eng_frq(s):
    frq = [0] * 26
    for c in s:
        if c in string.ascii_lowercase:
            frq[ord(c) - ord('a')] += 1
        elif c in string.ascii_uppercase:
            frq[ord(c) - ord('A')] += 1
    return frq

def cal_eng_frq_diff(frq):
    std_frq = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 
                0.02228, 0.02015, 0.06094, 0.06966, 0.00153,
                0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
                0.01929, 0.00095, 0.05987, 0.06327, 0.09056,
                0.02758, 0.00978, 0.02360, 0.00150, 0.01974,
                0.00074]
    tol = float(sum(frq))
    if tol == 0:
        return sys.maxint
    diff = 0
    for i in range(len(frq)):
        f = frq[i]/tol
        diff += (f - std_frq[i]) * (f - std_frq[i])
    return diff

def brk_fixed_iv_ctr(ciphers):
    key_stream = ''
    max_len = max(map(len, ciphers))
    for i in range(max_len):
        min_diff = sys.maxint
        key = 'a'
        col = ''
        for cipher in ciphers:
            if i < len(cipher):
                col += cipher[i]
        #print "col:", col
        for j in range(256):
            k = chr(j)
            s = xor_encrypt.xor_encrypt_str(col, k)
            #print "s:", s
            if not string_valid(s):
                continue
            frq = cal_eng_frq(s)
            diff = cal_eng_frq_diff(frq)
            #print ord(k), diff
            if diff < min_diff:
                key = k
                min_diff = diff
        key_stream += key
        if min_diff == sys.maxint:
            print "key in ", i, "is not found"
        #print "key:", ord(key)
    return key_stream

def main():
    key = my_rand.my_rand_str(16)
    iv = 0
    ciphers = []
    for plain in plains:
        plain = base64.b64decode(plain)
        cipher = ctr_mode.ctr_encrypt(key, iv, plain)
        ciphers.append(cipher)
    key_stream = brk_fixed_iv_ctr(ciphers)
    import binascii
    print binascii.hexlify(key_stream)
    print binascii.hexlify(ctr_mode.ctr_encrypt(key, iv, chr(0)*max(map(len, ciphers))))
    #for i in range(len(ciphers)):
    #    cipher = ciphers[i]
    #    plain = plains[i]
    #    print xor_encrypt.xor_encrypt_str(cipher, key_stream)
    #    print base64.b64decode(plain)

if __name__ == "__main__":
    main()
