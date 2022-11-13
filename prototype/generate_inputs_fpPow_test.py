import json
from splitToArray import split_to_arary

# Provide ints
# base = 15112345
# modulus = 615112345

# Or provide hexes
base_hex = '9139be98f16cf53d22da63cb559bb06a93338da6a344e28a4285c2da33facb7080d26e7a09483779a016eebc207602fc3f90492c2f2fb8143f0fe30fd855593d'
modulus_hex = '00cbfb45e6b09f1af40df60ddc865b6f98a1fd724678b583bfb5ae8539627bffdcd930d7c3f996f75e15172a017f143101ecd28fc629b800e24f0a83665d77c0a3'

base = int(base_hex, 16)
modulus = int(modulus_hex, 16)

base_array = split_to_arary(base, n=16, k=32)
modulus_array = split_to_arary(modulus, n=16, k=32)

print('base_array', base_array)
print('modulus_array', modulus_array)

print('out', pow(base, 65537, modulus))

input_json_dict = {
    'base': base_array,
    'modulus': modulus_array
}

with open("../input.json", "w") as outfile:
    outfile.write(json.dumps(input_json_dict))
