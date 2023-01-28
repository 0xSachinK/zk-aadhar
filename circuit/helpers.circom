pragma circom 2.1.0;

include "../node_modules/circomlib/circuits/bitify.circom";

function find_sub_array_return_first_index(_in, _in_len, sub_array, sub_array_len) {
    for (var i = 0; i < _in_len; i++) {
        var found = 1;
        for (var j = 0; j < sub_array_len; j++) {
            if (_in[i + j] != sub_array[j]) {
                found = 0;
                j = sub_array_len; // break;
            }
        }
        if (found) {
            return i;
        }
    }
    return -1;
}

function find_sub_array_return_last_index(_in, _in_len, sub_array, sub_array_len) {
    for (var i = 0; i < _in_len; i++) {
        var found = 1;
        for (var j = 0; j < sub_array_len; j++) {
            if (_in[i + j] != sub_array[j]) {
                found = 0;
                j = sub_array_len; // break;
            }
        }
        if (found) {
            return i + sub_array_len - 1;
        }
    }
    return -1;
}

template find_sub_array_return_values_in_between(
    _in, 
    _in_len, 
    sub_array_1, 
    sub_array_1_len, 
    sub_array_2, 
    sub_array_2_len,
    out_len
) {
    signal output out[out_len];
    
    var last_index = find_sub_array_return_last_index(_in, _in_len, sub_array_1, sub_array_1_len);
    // log("last_index: " , last_index , "");
    var first_index = find_sub_array_return_first_index(_in, _in_len, sub_array_2, sub_array_2_len);
    // log("first_index: " , first_index , "");

    for (var i = last_index + 1; i < last_index + 1 + out_len; i++) {
        out[i - last_index - 1] <-- _in[i];
    }
}



function base64LookUpTable(in)
{
    var out[6];

    if (in == 65)
        out = [0,0,0,0,0,0];        //	A
    else if (in == 66)
        out = [0,0,0,0,0,1];        //	B
    else if (in == 67)
        out = [0,0,0,0,1,0];        //	C
    else if (in == 68)
        out = [0,0,0,0,1,1];        //	D
    else if (in == 69)
        out = [0,0,0,1,0,0];        //	E
    else if (in == 70)
        out = [0,0,0,1,0,1];        //	F
    else if (in == 71)
        out = [0,0,0,1,1,0];        //	G
    else if (in == 72)
        out = [0,0,0,1,1,1];        //	H
    else if (in == 73)
        out = [0,0,1,0,0,0];        //	I
    else if (in == 74)
        out = [0,0,1,0,0,1];        //	J
    else if (in == 75)
        out = [0,0,1,0,1,0];        //	K
    else if (in == 76)
        out = [0,0,1,0,1,1];        //	L
    else if (in == 77)
        out = [0,0,1,1,0,0];        //	M
    else if (in == 78)
        out = [0,0,1,1,0,1];        //	N
    else if (in == 79)
        out = [0,0,1,1,1,0];        //	O
    else if (in == 80)
        out = [0,0,1,1,1,1];        //	P
    else if (in == 81)
        out = [0,1,0,0,0,0];        //	Q
    else if (in == 82)
        out = [0,1,0,0,0,1];        //	R
    else if (in == 83)
        out = [0,1,0,0,1,0];        //	S
    else if (in == 84)
        out = [0,1,0,0,1,1];        //	T
    else if (in == 85)
        out = [0,1,0,1,0,0];        //	U
    else if (in == 86)
        out = [0,1,0,1,0,1];        //	V
    else if (in == 87)
        out = [0,1,0,1,1,0];        //	W
    else if (in == 88)
        out = [0,1,0,1,1,1];        //	X
    else if (in == 89)
        out = [0,1,1,0,0,0];        //	Y
    else if (in == 90)
        out = [0,1,1,0,0,1];        //	Z
    else if (in == 91)
        out = [0,1,1,0,1,0];        //	a
    else if (in == 98)
        out = [0,1,1,0,1,1];        //	b
    else if (in == 99)
        out = [0,1,1,1,0,0];        //	c
    else if (in == 100)
        out = [0,1,1,1,0,1];        //	d
    else if (in == 101)
        out = [0,1,1,1,1,0];        //	e
    else if (in == 102)
        out = [0,1,1,1,1,1];        //	f
    else if (in == 103)
        out = [1,0,0,0,0,0];        //	g
    else if (in == 104)
        out = [1,0,0,0,0,1];        //	h
    else if (in == 105)
        out = [1,0,0,0,1,0];        //	i
    else if (in == 106)
        out = [1,0,0,0,1,1];        //	j
    else if (in == 107)
        out = [1,0,0,1,0,0];        //	k
    else if (in == 108)
        out = [1,0,0,1,0,1];        //	l
    else if (in == 109)
        out = [1,0,0,1,1,0];        //	m
    else if (in == 110)
        out = [1,0,0,1,1,1];        //	n
    else if (in == 111)
        out = [1,0,1,0,0,0];        //	o
    else if (in == 112)
        out = [1,0,1,0,0,1];        //	p
    else if (in == 113)
        out = [1,0,1,0,1,0];        //	q
    else if (in == 114)
        out = [1,0,1,0,1,1];        //	r
    else if (in == 115)
        out = [1,0,1,1,0,0];        //	s
    else if (in == 116)
        out = [1,0,1,1,0,1];        //	t
    else if (in == 117)
        out = [1,0,1,1,1,0];        //	u
    else if (in == 118)
        out = [1,0,1,1,1,1];        //	v
    else if (in == 119)
        out = [1,1,0,0,0,0];        //	w
    else if (in == 120)
        out = [1,1,0,0,0,1];        //	x
    else if (in == 121)
        out = [1,1,0,0,1,0];        //	y
    else if (in == 122)
        out = [1,1,0,0,1,1];        //	z
    else if (in == 48)
        out = [1,1,0,1,0,0];        //	0
    else if (in == 49)
        out = [1,1,0,1,0,1];        //	1
    else if (in == 50)
        out = [1,1,0,1,1,0];        //	2
    else if (in == 51)
        out = [1,1,0,1,1,1];        //	3
    else if (in == 52)
        out = [1,1,1,0,0,0];        //	4
    else if (in == 53)
        out = [1,1,1,0,0,1];        //	5
    else if (in == 54)
        out = [1,1,1,0,1,0];        //	6
    else if (in == 55)
        out = [1,1,1,0,1,1];        //	7
    else if (in == 56)
        out = [1,1,1,1,0,0];        //	8
    else if (in == 57)
        out = [1,1,1,1,0,1];        //	9
    else if (in == 43)
        out = [1,1,1,1,1,0];        //	+
    else if (in == 47)
        out = [1,1,1,1,1,1];        //	/

    return out;
}



// template split_to_array(n, k) {
//     signal input _in;
//     signal output out[k];
//     var pow = 2 ** n;
//     for (var i = 0; i < k; i++) {
//         out[i] <== _in % pow;
//         _in <== _in \ pow;
//     }
// }


// template TestHelpers() {

//     signal input in[9];
    
//     signal signature_node_start[3];
//     signature_node_start[0] <== 84;
//     signature_node_start[1] <== 87;
//     signature_node_start[2] <== 70;

//     signal signature_node_end[2];
//     signature_node_end[0] <== 111;
//     signature_node_end[1] <== 89;


//     component first_index_finder = find_sub_array_return_first_index(9, 3);
//     first_index_finder.in <== in;
//     first_index_finder.sub_array <== signature_node_start;

//     component last_index_finder = find_sub_array_return_first_index(9, 2);
//     last_index_finder.in <== in;
//     last_index_finder.sub_array <== signature_node_end;

//     log("first_index_finder.out", first_index_finder.out);
//     log("last_index_finder.out", last_index_finder.out);
    

//     var first_index = find_sub_array_return_first_index(_in, 9, sub_array, 3);
//     // log(first_index);

//     var last_index = find_sub_array_return_last_index(_in, 9, sub_array_end, 2);
//     // log(last_index);

//     component finder = find_sub_array_return_values_in_between(
//         _in, 9, sub_array, 3, sub_array_end, 2, 4
//     );

//     for (var i = 0; i < 4; i++) {
//         log(finder.out[i]);
//     }

//     var decimals_len = 4;

//     var base64_indices[decimals_len][6];

//     for (var i = 0; i < decimals_len; i++) {
//         var base64_index[6] = base64LookUpTable(finder.out[i]);
//         for (var j = 0; j < 6; j++) {
//             base64_indices[i][j] = base64_index[j];
//         }
//     }

//     for (var i = 0; i < decimals_len; i++) {
//         for (var j = 0; j < 6; j++) {
//             log(base64_indices[i][j]);
//         }
//     }

//     for (var i = 0; i < decimals_len; i++) {
//         log(base64_indices[i]);
//     }

//     var binary_arrays[decimals_len][6];

//     component num2Bits[decimals_len];
    
//     for (var i = 0; i < decimals_len; i++) {
//         num2Bits[i] = Num2Bits(6);
//     }

//     for (var i = 0; i < decimals_len; i++) {
//         var base64_index = base64_indices[i];
//         num2Bits[i].in <== 46;
//         for (var j = 0; j < 6; j++) {
//             binary_arrays[i][j] = num2Bits[i].out[j];
//         }
//     }

//     signal output out[decimals_len * 6];

//     for (var i = 0; i < decimals_len; i++) {
//         for (var j = 0; j < 6; j++) {
//             out[i * 6 + j] <== binary_arrays[i][j];
//         }
//     }

//     increases towards the right
//     for (var i = 0; i < 18; i++) {
//         log("out  ", out[i]);
//     }


//     signal output words[8];

//     component split_to_array = split_to_array(1, 8);
//     split_to_array._in <== x;
//     for (var i = 0; i < 8; i++) {
//         words[i] <== split_to_array.out[i];
//         log(words[i]);
//     }


//     signal input x;
//     signal input y;
//     signal output z;
//     z <== x * y;
// }

// component main = TestHelpers();