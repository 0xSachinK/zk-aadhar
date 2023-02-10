# read data from public.json
import json
data = None
with open('../../public.json', 'r') as f:
    data = json.loads(f.read())


out_binary_str = ''.join(data[:256])
out_hex_str = hex(int(out_binary_str, base=2))
print(out_hex_str)
