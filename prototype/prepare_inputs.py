
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

# Parse X509 certificate
x509_certificate_element = bs_data.find('X509Certificate')
x509_cert_value = x509_certificate_element.get_text()
x509_base64_decoded = base64.b64decode(x509_cert_value)
x509_hex_encoded = [hex(b) for b in x509_base64_decoded]

# Extract modulus from certificate
modulus_offset = 16 * 36 + 2
modulus_end = modulus_offset + 2048 // 8
modulus_hex_encoded = x509_hex_encoded[modulus_offset: modulus_end]
modulus_hex_str = convert_to_hex_string(modulus_hex_encoded)
modulus_int = int(modulus_hex_str, 16)
modulus_int_array = split_to_arary(modulus_int, n=n, k=k)

# Parse signature value
signature_value_element = bs_data.find('SignatureValue')
signature_value = signature_value_element.get_text()
signature_decoded = base64.b64decode(signature_value)
signature_hex_encoded = [hex(b) for b in signature_decoded]
signature_hex_str = convert_to_hex_string(signature_hex_encoded)
signature_int = int(signature_hex_str, 16)
signature_int_array = split_to_arary(signature_int, n=n, k=k)

# SHA1 of SHA256 UidData value
# Return uncanonicalized element
signed_info_element = bs_data.find('SignedInfo')

# Naive hacky canonicalization
digest_value_element = bs_data.find('DigestValue')
digest_value = digest_value_element.get_text()

digest_value_zeroes = [0 for _ in digest_value]
signed_info_element_canonicalized = f"""<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></DigestMethod><DigestValue>{digest_value}</DigestValue></Reference></SignedInfo>"""

signed_info_element_part_1 = """<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></DigestMethod><DigestValue>"""
signed_info_element_part_2 = """</DigestValue></Reference></SignedInfo>"""
print('\n')
print([ord(c) for c in signed_info_element_part_1])
print(digest_value_zeroes)
print([ord(c) for c in signed_info_element_part_2])
print('\n')

# Create padded base message
base_msg = hashlib.sha1(signed_info_element_canonicalized.encode()).hexdigest()
print("Base message:", base_msg, "\n")
padded_base_msg = pad_message(
    base_msg,
    'sha1',
    2048
)
print(padded_base_msg)
padded_base_msg_int = int(padded_base_msg, 16)
padded_base_msg_int_array = split_to_arary(padded_base_msg_int, n=n, k=k)
print("padded base message int array", padded_base_msg_int_array)

# Prpare digest value decoded
digest_val_decoded = base64.b64decode(digest_value)
digest_val_hex_encoded = [hex(b) for b in digest_val_decoded]
digest_val_hex_str = convert_to_hex_string(digest_val_hex_encoded)
print('Digest Value:', digest_val_hex_str, '\n')


# Remove Signature element from XML
signature_element = bs_data.find('Signature')
signature_element.decompose()

canonicalized_xml = str(bs_data)

# Perform naive cannonicalization
canonicalized_xml = canonicalized_xml\
    .replace('<?xml version="1.0" encoding="utf-8"?>', '')\
    .replace('/><Poa', '></Poi><Poa')\
    .replace('/><Pht', '></Poa><Pht')\
    .replace('\n', '')


# print(canonicalized_xml)
# Calculate SHA256 of canonicalized XML
sha256 = hashlib.sha256(canonicalized_xml.encode()).hexdigest()
print('SHA256 of canonicalized XML:', sha256, '\n')
digest_value_base64_decoded_hex_str = convert_to_hex_string(
    [hex(b) for b in base64.b64decode(digest_value)]
)
print('Digest value base64 decoded:', digest_value_base64_decoded_hex_str, '\n')
if digest_value_base64_decoded_hex_str == sha256:
    print('Digest value base64 decoded matches SHA256 of canonicalized XML')
# Note: Max ascii value is 127.


# Calculate SHA256 padding
sha256_padding = sha256_padding(len(canonicalized_xml))

# convert padding to binary string
sha256_padding_bin = ''.join(format(x, '08b') for x in sha256_padding)
print('SHA256 padding binary length:', len(sha256_padding_bin), '\n')

in_without_padding = [ord(c) for c in canonicalized_xml]

# convert all decimals in in_with_padding to binary
in_without_padding_binary_string = ''.join(
    format(x, '08b') for x in in_without_padding
)
print('Input without padding binary length:',
      len(in_without_padding_binary_string), '\n')

in_with_padding_binary_string = in_without_padding_binary_string + sha256_padding_bin
print('Input with padding binary length:',
      len(in_with_padding_binary_string), '\n')

# Assert length % 512 == 0
assert len(in_with_padding_binary_string) % 512 == 0

# Suggest length of input in bits
# Add 10% to the length of the input and round up to the nearest multiple of 512
suggested_length = int(len(in_with_padding_binary_string) * 1.1)
suggested_length = suggested_length + (512 - suggested_length % 512)
print('Suggested length:', suggested_length, '\n')

# Add 0s to the end of in_with_padding_binary_string until it is the suggested length
in_with_padding_binary_string = in_with_padding_binary_string + \
    '0' * (suggested_length - len(in_with_padding_binary_string))
print('Input with padding binary length:',
      len(in_with_padding_binary_string), '\n')


# Sha256 verification inputs
# input_json_dict = {
#     'in_padded': [b for b in in_with_padding_binary_string],
#     'in_len_padded_bits': len(in_with_padding_binary_string),
# }

print("Num chars", len(signed_info_element_canonicalized))


in_bits = [d for d in bin(int(base_msg, 16))[2:]]
print("Num bits", len(in_bits))
# append 0s to the beginning of in_bits until it is 160 bits long
in_bits = ['0'] * (160 - len(in_bits)) + in_bits

# Sha1 Verificaiton inputs
input_json_dict = {
    "in_bits": in_bits,
    "x": 2,
    "y": 3
}

with open("../input.json", "w") as outfile:
    outfile.write(json.dumps(input_json_dict))
