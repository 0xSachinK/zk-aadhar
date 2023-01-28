import base64
import json
import hashlib
from lxml import etree
from bs4 import BeautifulSoup
from splitToArray import split_to_arary
from utils import convert_to_hex_string
from pad_base_message import pad_message

# Circuit parameters
n = 50
k = 41

###### OPEN QUESTIONS #######
# Why is the digest valule different in canonicalized and non-canonicalized formats?
# How did I get that signature value that I have in the screenshot?

# I might find answers in windows machine.
#############################

input_file_path = '../../node_scripts/offlineaadhaar20220917094619777.xml'
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
print('Modulus:', modulus_hex_str, '\n')
modulus_int = int(modulus_hex_str, 16)
modulus_int_array = split_to_arary(modulus_int, n=n, k=k)

# Parse signature value
signature_value_element = bs_data.find('SignatureValue')
signature_value = signature_value_element.get_text()
signature_decoded = base64.b64decode(signature_value)
print(signature_decoded)
signature_hex_encoded = [hex(b) for b in signature_decoded]
signature_hex_str = convert_to_hex_string(signature_hex_encoded)
print('Signature:', signature_hex_str, '\n')
signature_int = int(signature_hex_str, 16)
print('Signature int', signature_int)
signature_int_array = split_to_arary(signature_int, n=n, k=k)

# SHA1 of SHA256 UidData value
# Return uncanonicalized element
signed_info_element = bs_data.find('SignedInfo')

# Naive hacky canonicalization
digest_value_element = bs_data.find('DigestValue')
digest_value = digest_value_element.get_text()
print('Digest value', digest_value)
signed_info_element_canonicalized = f"""<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></DigestMethod><DigestValue>{digest_value}</DigestValue></Reference></SignedInfo>"""
base_msg = hashlib.sha1(signed_info_element_canonicalized.encode()).hexdigest()
print('Base Message:', base_msg, '\n')

# Pad digest value to create base message
padded_base_msg = pad_message(
    base_msg,
    'sha1',
    2048
)
padded_base_msg_int = int(padded_base_msg, 16)
padded_base_msg_int_array = split_to_arary(padded_base_msg_int, n=n, k=k)
print(padded_base_msg_int_array)

input_json_dict = {
    'signature': signature_int_array,
    'modulus': modulus_int_array,
    'padded_message': padded_base_msg_int_array
}

with open("../input.json", "w") as outfile:
    outfile.write(json.dumps(input_json_dict))


# with open('processedaadhar.xml', 'w') as f:
#     f.write(obj_xml_str)

# Parse digest value
# Note: This is the sha256 of UidData and not the input
# to the signature.

# digest_val_decoded = base64.b64decode(digest_value)
# digest_val_hex_encoded = [hex(b) for b in digest_val_decoded]
# digest_val_hex_str = convert_to_hex_string(digest_val_hex_encoded)
# print('Digest Value:', digest_val_hex_str, '\n')

# offline_paper_ekyc = bs_data.find('OfflinePaperlessKyc')
# tree = etree.fromstring(str(offline_paper_ekyc))
# signature_element = tree.find('{http://www.w3.org/2000/09/xmldsig#}Signature')
# # print(etree.tostring(signature_element))

# signed_info_element = tree.find('SignedInfo')
# print(signed_info_element)

# tree.remove(signature_element)
# obj_xml = etree.tostring(tree)
# obj_xml_str = '<?xml version="1.0" encoding="UTF-8"?>' + obj_xml.decode('utf-8')
# uid_data_decimal_array = [ord(c) for c in obj_xml_str]
# sha256_bits = []
# sha1_digest_int_array = []
