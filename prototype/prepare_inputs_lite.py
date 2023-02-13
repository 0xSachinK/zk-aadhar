
import xml.dom.minidom
import base64
import json
import hashlib
from lxml import etree
from bs4 import BeautifulSoup

from utils import convert_to_hex_string, sha256_padding, split_to_arary, pad_message

# Circuit parameters
n = 50
k = 41


input_file_path = '../aadhaar_files/offlineaadhaar20220917094619777.xml'
data = None
with open(input_file_path, 'r') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')

#
# Parse signature value
#
signature_value_element = bs_data.find('SignatureValue')
signature_value = signature_value_element.get_text()
signature_decoded = base64.b64decode(signature_value)
signature_hex_encoded = [hex(b) for b in signature_decoded]
signature_hex_str = convert_to_hex_string(signature_hex_encoded)
signature_int = int(signature_hex_str, 16)
signature_int_array = split_to_arary(signature_int, n=n, k=k)

#
# Parse DigestValue
#
digest_value_element = bs_data.find('DigestValue')
digest_value = digest_value_element.get_text()

#
# Parse OfflinePaperlessKyc
#
input_file_path = '../aadhaar_files/CanonicalizedSignatureRemoved.xml'
offlinepaperlesskyc_data = None
with open(input_file_path, 'r') as f:
    offlinepaperlesskyc_data = f.read()


def sha256Padding(message):
    # convert the message to a bit array
    message_bits = []
    for i in range(len(message)):
        char = ord(message[i])
        for j in range(7, -1, -1):
            message_bits.append((char >> j) & 1)

    # add the 1-bit to the end of the message
    message_bits.append(1)

    # add 0-bits to the end of the message until it is congruent to 448 modulo 512
    while len(message_bits) % 512 != 448:
        message_bits.append(0)

    # add the original length of the message (in bits) to the end of the padded message
    message_length = len(message) * 8
    for i in range(63, -1, -1):
        message_bits.append((message_length >> i) & 1)

    # TODO: HACK FOR NOW!!!! Not required in python.
    # Set the 471th bit to 0
    # message_bits[-41] = 0

    return message_bits


N = 69632
offlinepaperlesskyc_padded = sha256Padding(offlinepaperlesskyc_data)

# Assert length % 512 == 0
assert len(offlinepaperlesskyc_padded) % 512 == 0

# Extend offlinepaperlesskyc_padded list to 69632 bits
offlinepaperlesskyc_padded_with_zeroes = offlinepaperlesskyc_padded + \
    [0] * (N - len(offlinepaperlesskyc_padded))

assert len(offlinepaperlesskyc_padded_with_zeroes) == N

# signal input OfflinePaperlessKyc_padded_bits[N];
# signal input OfflinePaperlessKyc_padded_bits_len;
# signal input DigestValue[44];
# signal input signature[41];

# Sha256 verification inputs
input_json_dict = {
    'OfflinePaperlessKyc_padded_bits': offlinepaperlesskyc_padded_with_zeroes,
    'OfflinePaperlessKyc_padded_bits_len': len(offlinepaperlesskyc_padded),
    'DigestValue': [ord(c) for c in digest_value],
    'signature': [str(c) for c in signature_int_array]
}


with open("../input.json", "w") as outfile:
    outfile.write(json.dumps(input_json_dict))
