import random
import struct  # for struct.pack


def convert_to_hex_string(hex_array):
    hex_str_array = []
    for h in hex_array:
        c = h[2:]
        if len(c) == 1:
            c = '0' + c
        hex_str_array.append(c)
    return ''.join(hex_str_array)


def sha256_padding(input_len):
    """Calculate SHA256 padding for given input length."""
    # https://tools.ietf.org/html/rfc6234#section-4.1
    padding = bytearray()
    # Append 0x80
    padding.append(0x80)
    # Append 0x00 until length is 56 mod 64
    while (input_len + len(padding)) % 64 != 56:
        padding.append(0x00)
    # Append 64 bit big endian length
    # big endian = most significant byte first
    # >Q = unsigned long long and is 8 bytes (64 bits)
    padding.extend(struct.pack('>Q', input_len * 8))
    return padding


# k chunks of n bits

def split_to_arary(_in, n, k):
    _in_copy = _in
    words = [0 for _ in range(k)]
    for i in range(k):
        words[i] = _in % 2 ** n
        _in = _in // 2 ** n     # // is used to get an integer back from division of two ints

    if _in != 0:
        raise Exception(f'Number {_in_copy} does not fit in {k * n} bits')

    # do not reverse. Keep least signficant bit as the first index.
    return words


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


asn1_bytes = {
    'sha1': '3021300906052b0e03021a05000414'
}


def pad_message(base_message, signature_scheme, output_len):
    asn1_byte_str = asn1_bytes[signature_scheme]
    ff_octet_str_length = output_len // 8 - (
        len(asn1_byte_str)
        + len(base_message)
        + 6  # 0001 and 00
    ) // 2
    ff_octet_str = 'ff' * ff_octet_str_length
    padded_base_message = '0001' + ff_octet_str + '00' + asn1_byte_str + base_message
    return padded_base_message


# base_message = '8c723a0fa70b111017b4a6f06afe1c0dbcec14e3'
# padded_base_message = pad_message(base_message, 'sha1', 2048)
# print(padded_base_message)
