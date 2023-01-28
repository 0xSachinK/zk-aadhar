from nodes import signature_value_node_start, signature_value_node_end, digest_value_node_start, digest_value_node_end
from utils import find_sub_array_return_values_in_between
import hashlib


def base64_decoder(decimals):
    # create the Base64 lookup table
    base64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # convert decimal values to their corresponding ASCII characters
    ascii_chars = [chr(decimal) for decimal in decimals]

    # map the ASCII characters to their corresponding Base64 indices
    base64_indices = []

    for char in ascii_chars:
        if char not in base64_table:
            print('char', char, 'not in base64_table')
            continue
        base64_indices.append(base64_table.index(char))

    # convert the Base64 indices to binary arrays of length 6
    binary_arrays = [format(index, '06b') for index in base64_indices]

    # concatenate the binary arrays together
    binary_string = ''.join(binary_arrays)

    return binary_string


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


def num2Bits(_in, n):
    out = [0 for i in range(n)]
    for i in range(n):
        out[i] = (_in >> i) & 1
    # Note: 5 is 1010 instead of, 0101.
    # That is the most significant bit is on the right (last element of out)
    return out


def bits2Num(_in):
    # Most significant should be the last element of the input array.
    out = 0
    e2 = 1
    for i in _in:
        out += i * e2
        e2 = 2 * e2
    return out


n = 50
k = 41

input_file_path = '../../node_scripts/offlineaadhaar20220917094619777.xml'
data = None
with open(input_file_path, 'r') as f:
    data = f.read()

data = data.replace('&#13;', '')

# Convert every character to its ASCII decimal value
data = [ord(c) for c in data]

# First we extract the signature
signature = find_sub_array_return_values_in_between(
    data,
    signature_value_node_start,
    signature_value_node_end
)

signature_base64_decoded_binary_string = base64_decoder(signature)
signature_base64_decoded_binary_string = [
    int(c) for c in signature_base64_decoded_binary_string]
signature_int_value = bits2Num(
    signature_base64_decoded_binary_string[::-1][4:]
)
print('signature int value', signature_int_value)

signature_int_array = split_to_arary(signature_int_value, n=n, k=k)
print(signature_int_array)

# Extract digest value
digest_value = find_sub_array_return_values_in_between(
    data,
    digest_value_node_start,
    digest_value_node_end
)
digest_value_base64_str = ''.join([chr(c) for c in digest_value])

signed_info_element_canonicalized = f"""<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></DigestMethod><DigestValue>{digest_value_base64_str}</DigestValue></Reference></SignedInfo>"""
base_msg = hashlib.sha1(signed_info_element_canonicalized.encode()).hexdigest()

# Pad digest value to create base message
padded_base_msg = pad_message(
    base_msg,
    'sha1',
    2048
)
padded_base_msg_int = int(padded_base_msg, 16)
padded_base_msg_int_array = split_to_arary(padded_base_msg_int, n=n, k=k)
print(padded_base_msg_int_array)
