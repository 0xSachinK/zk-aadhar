from splitToArray import split_to_arary
import json

n = 50
k = 41




modulus_hex_str = 'c674b80a6eeeb4cc68f334bac04c3678761e8f8a2c3fb0b4448bd3997475c798f54686a2f28ee22ec59eee246f6d29ee69bac5a4559c2ecd6230bac3187ac73ba90984c2e81f9ccf274b233d3cefad49f0da92ba733187691df395fce6ceaaf819282ed46a76ee902b3180522f65e51419111e25a15d4b24f59971ef9d99f435'
modulus_int = int(modulus_hex_str, 16)
modulus_array = split_to_arary(modulus_int, n=n, k=k)      # 64 * 8 = 512 bit

padded_hash_hex_str = '0001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff003021300906052b0e03021a050004148c723a0fa70b111017b4a6f06afe1c0dbcec14e3'
padded_hash_int = int(padded_hash_hex_str, 16)
padded_hash_array = split_to_arary(padded_hash_int, n=n, k=k)

signature_hex_str = '78fddb31f579adad90da81d6d5fcf70cffea4b14ae09708c479421f3e3bfc46b70e0a97ce13268732733104212062e1c2915dd9b485fd3d2cbb53f3b6592a209e1cbfe5281b0d7034be85af3b5a6ac9b103bf2d7fd96bd4ed9fdd2b47db650e8a1e459ce4936ed002eee48c964730f89933c43765a7b11c89ed2a4dfa6fc44d5'
signature_int = int(signature_hex_str, 16)
signature_array = split_to_arary(signature_int, n=n, k=k)

padded_hash_out_int = pow(signature_int, 65537, modulus_int)
padded_hash_out_hex = hex(padded_hash_out_int)
padded_hash_out_array = split_to_arary(padded_hash_out_int, n=n, k=k)
print('Padded Hash Out Int', padded_hash_out_int)
print('Padded Hash out hex', padded_hash_hex_str)
print('Padded Hash array split', padded_hash_out_array)


input_json_dict = {
    'signature': signature_array,
    'modulus': modulus_array,
    'padded_message': padded_hash_array 
}



with open("../input.json", "w") as outfile:
    outfile.write(json.dumps(input_json_dict))
