from splitToArray import split_to_arary, array_to_int
import json

# modulus_hex_str = '00cbfb45e6b09f1af40df60ddc865b6f98a1fd724678b583bfb5ae8539627bffdcd930d7c3f996f75e15172a017f143101ecd28fc629b800e24f0a83665d77c0a3'
# modulus_int = int(modulus_hex_str, 16)
# modulus_array = split_to_arary(modulus_int, n=64, k=8)      # 64 * 8 = 512 bit
# modulus_reconstructed_val = array_to_int(modulus_array, n=64)
# assert modulus_reconstructed_val == modulus_int

# padded_hash_hex_str = '0001ffffffffffffffffffffffffffffffffffffffffffffffffffff003021300906052b0e03021a050004148c723a0fa70b111017b4a6f06afe1c0dbcec14e3'
# padded_hash_int = int(padded_hash_hex_str, 16)
# padded_hash_array = split_to_arary(padded_hash_int, n=64, k=8)
# padded_hash_reconstructed_val = array_to_int(padded_hash_array, n=64)
# # assert padded_hash_reconstructed_val == padded_hash_int

# signature_hex_str = '9139be98f16cf53d22da63cb559bb06a93338da6a344e28a4285c2da33facb7080d26e7a09483779a016eebc207602fc3f90492c2f2fb8143f0fe30fd855593d'
# signature_int = int(signature_hex_str, 16)
# signature_array = split_to_arary(signature_int, n=64, k=8)
# signature_reconstructed_val = array_to_int(signature_array, n=64)
# # assert signature_reconstructed_val == signature_int

# padded_hash_out_int = pow(signature_int, 65537, modulus_int)
# padded_hash_out_hex = hex(padded_hash_out_int)
# padded_hash_out_array = split_to_arary(padded_hash_out_int, n=64, k=8)
# print('Padded Hash Out Int', padded_hash_out_int)
# print('Padded Hash out hex', padded_hash_hex_str)
# print('Padded Hash array split', padded_hash_out_array)

out_array = [5347,48364,7181,27390,42736,6068,4368,42763,14863,35954,1044,1280,538,3587,1323,2310,8496,48,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,65535,1]

val = array_to_int(out_array, 16)
print('Integer', val)
print('Hex    ', f'{val:0x}')
# 409173825987017733751648712103449894027080255755383098685411420515058722331761614033343349191150215048257865372193312126743148306355620847721405748451
# 6254606875367089264366455805545352797233819021337670996585430826833112507799508623130268961759327103138769764478477153061967471121136135396804264898232320