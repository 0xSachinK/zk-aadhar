import random

# k chunks of n bits
def split_to_arary(_in, n, k):
    _in_copy = _in
    words = [0 for _ in range(k)]
    for i in range(k):
        words[i] = _in % 2 ** n
        _in = _in // 2 ** n     # // is used to get an integer back from division of two ints
    
    if _in != 0:
        raise Exception(f'Number {_in_copy} does not fit in {k * n} bits')

    return  words    # do not reverse. Keep least signficant bit as the first index.

def array_to_int(_in, n):
    k = len(_in)
    base = 2 ** n
    out = 0
    for i in range(k):
        out += _in[i] * (base ** i)
    return out

# _in = random.randint(1, 2 ** 64)
# n = 64
# k = 8
# out_arr = split_to_arary(_in, n, k)
# print(out_arr, '\n')
# reconstructed_in = array_to_int(out_arr, n)
# print(_in, '\n')
# print(reconstructed_in, '\n')
# assert reconstructed_in == _in

