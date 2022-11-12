
pragma circom 2.0.0;

include "./base64decoder.circom";

template Base64Test() {

    signal input x;
    signal output y;
    
    var _x = x;
    var lookup_val = base64LookUpTable(_x);

    y <-- lookup_val;
    y === 63;
}

component main = Base64Test();