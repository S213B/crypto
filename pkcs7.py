import binascii

def pkcs7_pad(input, block_size):
    l = len(input)
    remainder = l % block_size
    if remainder == 0:
        return input
    padding = block_size - remainder
    return input + chr(padding) * padding

def pkcs7_unpad(input, block_size):
    padding = input[-1]
    cnt = ord(padding)
    if cnt >= block_size:
        return input
    if input[-cnt:] == padding * cnt:
        return input[:-cnt]
    else:
        return input


if __name__ == "__main__":
    plaintext = "YELLOW SUBMARINE"
    text = pkcs7_pad(plaintext, 10)
    print binascii.hexlify(plaintext)
    print binascii.hexlify(text)
