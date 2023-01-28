
# def base64LookUpTable(_in):

#     out = None

#     if (_in == 65):
#         out = 0  # 000000	A
#     elif (_in == 66):
#         out = 1  # 000001	B
#     elif (_in == 67):
#         out = 2  # 000010	C
#     elif (_in == 68):
#         out = 3  # 000011	D
#     elif (_in == 69):
#         out = 4  # 000100	E
#     elif (_in == 70):
#         out = 5  # 000101	F
#     elif (_in == 71):
#         out = 6  # 000110	G
#     elif (_in == 72):
#         out = 7  # 000111	H
#     elif (_in == 73):
#         out = 8  # 001000	I
#     elif (_in == 74):
#         out = 9  # 001001	J
#     elif (_in == 75):
#         out = 10  # 001010	K
#     elif (_in == 76):
#         out = 11  # 001011	L
#     elif (_in == 77):
#         out = 12  # 001100	M
#     elif (_in == 78):
#         out = 13  # 001101	N
#     elif (_in == 79):
#         out = 14  # 001110	O
#     elif (_in == 80):
#         out = 15  # 001111	P
#     elif (_in == 81):
#         out = 16  # 010000	Q
#     elif (_in == 82):
#         out = 17  # 010001	R
#     elif (_in == 83):
#         out = 18  # 010010	S
#     elif (_in == 84):
#         out = 19  # 010011	T
#     elif (_in == 85):
#         out = 20  # 010100	U
#     elif (_in == 86):
#         out = 21  # 010101	V
#     elif (_in == 87):
#         out = 22  # 010110	W
#     elif (_in == 88):
#         out = 23  # 010111	X
#     elif (_in == 89):
#         out = 24  # 011000	Y
#     elif (_in == 90):
#         out = 25  # 011001	Z
#     elif (_in == 97):
#         out = 26  # 011010	a
#     elif (_in == 98):
#         out = 27  # 011011	b
#     elif (_in == 99):
#         out = 28  # 011100	c
#     elif (_in == 100):
#         out = 29  # 011101	d
#     elif (_in == 101):
#         out = 30  # 011110	e
#     elif (_in == 102):
#         out = 31  # 011111	f
#     elif (_in == 103):
#         out = 32  # 100000	g
#     elif (_in == 104):
#         out = 33  # 100001	h
#     elif (_in == 105):
#         out = 34  # 100010	i
#     elif (_in == 106):
#         out = 35  # 100011	j
#     elif (_in == 107):
#         out = 36  # 100100	k
#     elif (_in == 108):
#         out = 37  # 100101	l
#     elif (_in == 109):
#         out = 38  # 100110	m
#     elif (_in == 110):
#         out = 39  # 100111	n
#     elif (_in == 111):
#         out = 40  # 101000	o
#     elif (_in == 112):
#         out = 41  # 101001	p
#     elif (_in == 113):
#         out = 42  # 101010	q
#     elif (_in == 114):
#         out = 43  # 101011	r
#     elif (_in == 115):
#         out = 44  # 101100	s
#     elif (_in == 116):
#         out = 45  # 101101	t
#     elif (_in == 117):
#         out = 46  # 101110	u
#     elif (_in == 118):
#         out = 47  # 101111	v
#     elif (_in == 119):
#         out = 48  # 110000	w
#     elif (_in == 120):
#         out = 49  # 110001	x
#     elif (_in == 121):
#         out = 50  # 110010	y
#     elif (_in == 122):
#         out = 51  # 110011	z
#     elif (_in == 48):
#         out = 52  # 110100	0
#     elif (_in == 49):
#         out = 53  # 110101	1
#     elif (_in == 50):
#         out = 54  # 110110	2
#     elif (_in == 51):
#         out = 55  # 110111	3
#     elif (_in == 52):
#         out = 56  # 111000	4
#     elif (_in == 53):
#         out = 57  # 111001	5
#     elif (_in == 54):
#         out = 58  # 111010	6
#     elif (_in == 55):
#         out = 59  # 111011	7
#     elif (_in == 56):
#         out = 60  # 111100	8
#     elif (_in == 57):
#         out = 61  # 111101	9
#     elif (_in == 43):
#         out = 62  # 111110	+
#     elif (_in == 47):
#         out = 63  # 111111	/
#     elif (_in == 61):
#         out = 0     # 000000    = (padding)

#     return out


# def decodeBase64(_in):
#     decoded_base64 = []
#     for i in _in:
#         x = base64LookUpTable(i)
#         decoded_base64.append(x)
#         if x is None:
#             print(i, x)

#     bits = []
#     for dec in decoded_base64:
#         _bits = num2Bits(dec, 6)
#         print(_bits)
#         reversed_bits = _bits[::-1]
#         bits.extend(reversed_bits)

#     out = []
#     i = 0
#     while i < len(bits):
#         _bits = bits[i:i+8]
#         # reverese the bits for input to bits2Num
#         reveresed_bits = _bits[::-1]
#         num = bits2Num(reveresed_bits, 8)
#         out.append(num)
#         i += 8
#     return out


# # _in = [84, 87, 70, 117, 101, 83, 66, 111, 89, 87, 53, 107, 99, 121, 66, 116, 89, 87,
# #        116, 108, 73, 71, 120, 112, 90, 50, 104, 48, 73, 72, 100, 118, 99, 109, 115, 117]

# # # convert _in to a string
# # in_str = ''.join([chr(i) for i in _in])
# # print(in_str)

# # out = decodeBase64(_in)
# # print(out)

# # # convert in to a string
# # out_str = ''.join([chr(i) for i in out])
# # print(out_str)
