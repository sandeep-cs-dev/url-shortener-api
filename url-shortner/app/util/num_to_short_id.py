from sqids import Sqids

# sqids = Sqids()
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

sqids = Sqids(alphabet=alphabet, min_length=6)


# [1,2,3] -> 86Rf07
def encode_num(numbers):
    return sqids.encode(numbers)


# 86Rf07 -> [1,2,3]
def decode_num(encode_numbers):
    return sqids.decode(encode_numbers)


# Base62 character set

def base62_encode(num):
    if num == 0:
        return alphabet[0]
    base62 = []
    while num > 0:
        num, rem = divmod(num, 62)
        base62.append(alphabet[rem])
    return ''.join(reversed(base62))


def base62_decode(s):
    num = 0
    for char in s:
        num = num * 62 + alphabet.index(char)
    return num
