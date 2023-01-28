def convert_to_hex_string(hex_array):
    hex_str_array = []
    for h in hex_array:
        c = h[2:]
        if len(c) == 1:
            c = '0' + c
        hex_str_array.append(c)
    return ''.join(hex_str_array)