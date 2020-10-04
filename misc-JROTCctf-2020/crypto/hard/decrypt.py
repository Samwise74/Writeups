plain = open('plain1.txt', 'r')
ctxt = open('crypt1.enc', 'rb')
sample = open('sample.enc', 'rb')


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


key = byte_xor(plain.read().encode(), ctxt.read())
flag = byte_xor(sample.read(), key)

print(flag)
