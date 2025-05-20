
alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
# [1,2,3] -> 86Rf07
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
