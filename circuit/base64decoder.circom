pragma circom 2.0.0;

function base64LookUpTable(in)
{
    var out;

    if (in == 65)
        out = 0;	// 000000	A
    else if (in == 66)
        out = 1;	// 000001	B
    else if (in == 67)
        out = 2;	// 000010	C
    else if (in == 68)
        out = 3;	// 000011	D
    else if (in == 69)
        out = 4;	// 000100	E
    else if (in == 70)
        out = 5;	// 000101	F
    else if (in == 71)
        out = 6;	// 000110	G
    else if (in == 72)
        out = 7;	// 000111	H
    else if (in == 73)
        out = 8;	// 001000	I
    else if (in == 74)
        out = 9;	// 001001	J
    else if (in == 75)
        out = 10;	// 001010	K
    else if (in == 76)
        out = 11;	// 001011	L
    else if (in == 77)
        out = 12;	// 001100	M
    else if (in == 78)
        out = 13;	// 001101	N
    else if (in == 79)
        out = 14;	// 001110	O
    else if (in == 80)
        out = 15;	// 001111	P
    else if (in == 81)
        out = 16;	// 010000	Q
    else if (in == 82)
        out = 17;	// 010001	R
    else if (in == 83)
        out = 18;	// 010010	S
    else if (in == 84)
        out = 19;	// 010011	T
    else if (in == 85)
        out = 20;	// 010100	U
    else if (in == 86)
        out = 21;	// 010101	V
    else if (in == 87)
        out = 22;	// 010110	W
    else if (in == 88)
        out = 23;	// 010111	X
    else if (in == 89)
        out = 24;	// 011000	Y
    else if (in == 90)
        out = 25;	// 011001	Z
    else if (in == 91)
        out = 26;	// 011010	a
    else if (in == 98)
        out = 27;	// 011011	b
    else if (in == 99)
        out = 28;	// 011100	c
    else if (in == 100)
        out = 29;	// 011101	d
    else if (in == 101)
        out = 30;	// 011110	e
    else if (in == 102)
        out = 31;	// 011111	f
    else if (in == 103)
        out = 32;	// 100000	g
    else if (in == 104)
        out = 33;	// 100001	h
    else if (in == 105)
        out = 34;	// 100010	i
    else if (in == 106)
        out = 35;	// 100011	j
    else if (in == 107)
        out = 36;	// 100100	k
    else if (in == 108)
        out = 37;	// 100101	l
    else if (in == 109)
        out = 38;	// 100110	m
    else if (in == 110)
        out = 39;	// 100111	n
    else if (in == 111)
        out = 40;	// 101000	o
    else if (in == 112)
        out = 41;	// 101001	p
    else if (in == 113)
        out = 42;	// 101010	q
    else if (in == 114)
        out = 43;	// 101011	r
    else if (in == 115)
        out = 44;	// 101100	s
    else if (in == 116)
        out = 45;	// 101101	t
    else if (in == 117)
        out = 46;	// 101110	u
    else if (in == 118)
        out = 47;	// 101111	v
    else if (in == 119)
        out = 48;	// 110000	w
    else if (in == 120)
        out = 49;	// 110001	x
    else if (in == 121)
        out = 50;	// 110010	y
    else if (in == 122)
        out = 51;	// 110011	z
    else if (in == 48)
        out = 52;	// 110100	0
    else if (in == 49)
        out = 53;	// 110101	1
    else if (in == 50)
        out = 54;	// 110110	2
    else if (in == 51)
        out = 55;	// 110111	3
    else if (in == 52)
        out = 56;	// 111000	4
    else if (in == 53)
        out = 57;	// 111001	5
    else if (in == 54)
        out = 58;	// 111010	6
    else if (in == 55)
        out = 59;	// 111011	7
    else if (in == 56)
        out = 60;	// 111100	8
    else if (in == 57)
        out = 61;	// 111101	9
    else if (in == 43)
        out = 62;	// 111110	+
    else if (in == 47)
        out = 63;	// 111111	/

    return out;
}