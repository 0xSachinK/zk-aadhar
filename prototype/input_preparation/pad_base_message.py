asn1_bytes = {
    'sha1': '3021300906052b0e03021a05000414'
}
    

def pad_message(base_message, signature_scheme, output_len):
    asn1_byte_str = asn1_bytes[signature_scheme]
    ff_octet_str_length = output_len // 8 - (
            len(asn1_byte_str) 
            + len(base_message) 
            + 6 # 0001 and 00
        ) // 2
    ff_octet_str = 'ff' * ff_octet_str_length
    padded_base_message = '0001' + ff_octet_str + '00' + asn1_byte_str + base_message
    return padded_base_message


# base_message = '8c723a0fa70b111017b4a6f06afe1c0dbcec14e3'
# padded_base_message = pad_message(base_message, 'sha1', 2048)
# print(padded_base_message)