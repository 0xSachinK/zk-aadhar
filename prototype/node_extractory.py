
start_tag_starter = 60
tag_ender = 62
end_tag_starter = [60, 47]
OfflinePaperlessKyc = [79, 102, 102, 108, 105, 110, 101, 80, 97, 112, 101, 114, 108, 101, 115, 115, 75, 121, 99]    # len = 19
Signature = [83, 105, 103, 110, 97, 116, 117, 114, 101]     # len = 9
SignedInfo = [83, 105, 103, 110, 101, 100, 73, 110, 102, 111]       # len = 10
KeyInfo = [75, 101, 121, 73, 110, 102, 111]     # len = 7
X509Data = [88, 53, 48, 57, 68, 97, 116, 97]        # len = 8s
X509SubjectName = [88, 53, 48, 57, 83, 117, 98, 106, 101, 99, 116, 78, 97, 109, 101]    # len = 15
X509Certificate = [88, 53, 48, 57, 67, 101, 114, 116, 105, 102, 105, 99, 97, 116, 101]  # len = 15


def parse_node(_in, node_tag):

    i = 0
    n = len(node_tag)
    out = []

    while i < len(_in):
        if _in[i] == start_tag_starter:
            if _in[i + n + 1] == tag_ender:
                k = 0
                while k < n:
                    print(_in[i + 1 + k], node_tag[k])
                    if _in[i + 1 + k] != node_tag[k]:
                        break
                    k += 1
                if k == n:
                    # Found
                    # Now return the elements within the tag
                    x = i + n + 2 # Additional 2 to account for the tags at beginning and end < and >
                    while _in[x:x+2] != end_tag_starter:
                        out.append(_in[x])
                        x += 1
                    return out
        i += 1  
      


aadhar_xml = "<xml><UidData>name='sachin' age=18 country='india'</UidData><xyzABC>1234</xyzABC></xml>"
aadhar_xml_ascii_decoded = [ord(c) for c in aadhar_xml]
node_tag_str = 'UidData'
node_tag_ascii_decoded = [ord(c) for c in node_tag_str]
parsed_node_data_decimal_format = parse_node(aadhar_xml_ascii_decoded, node_tag_ascii_decoded)
parsed_node_string_format = [chr(d) for d in parsed_node_data_decimal_format]
print(''.join(parsed_node_string_format))