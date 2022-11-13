from splitToArray import split_to_arary
import json

modulus_hex_str = '00cbfb45e6b09f1af40df60ddc865b6f98a1fd724678b583bfb5ae8539627bffdcd930d7c3f996f75e15172a017f143101ecd28fc629b800e24f0a83665d77c0a3'
modulus_int = int(modulus_hex_str, 16)
modulus_array = split_to_arary(modulus_int, n=16, k=32)      # 64 * 8 = 512 bit

padded_hash_hex_str = '0001ffffffffffffffffffffffffffffffffffffffffffffffffffff003021300906052b0e03021a050004148c723a0fa70b111017b4a6f06afe1c0dbcec14e3'
padded_hash_int = int(padded_hash_hex_str, 16)
padded_hash_array = split_to_arary(padded_hash_int, n=16, k=32)

signature_hex_str = '9139be98f16cf53d22da63cb559bb06a93338da6a344e28a4285c2da33facb7080d26e7a09483779a016eebc207602fc3f90492c2f2fb8143f0fe30fd855593d'
signature_int = int(signature_hex_str, 16)
signature_array = split_to_arary(signature_int, n=16, k=32)

padded_hash_out_int = pow(signature_int, 65537, modulus_int)
padded_hash_out_hex = hex(padded_hash_out_int)
padded_hash_out_array = split_to_arary(padded_hash_out_int, n=16, k=32)
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
