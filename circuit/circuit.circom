
pragma circom 2.0.0;

include "./base64decoder.circom";
include "../helper-circuits/fp.circom";
include "../helper-circuits/rsa.circom";
include "../node_modules/circomlib/circuits/sha256/sha256.circom";


template Base64Test() {
    signal input x;
    signal output y;
    
    var _x = x;
    var lookup_val = base64LookUpTable(_x);

    y <-- lookup_val;
    y === 63;
}

template MyRSAVerify65537(n, k) {
    signal input signature[k];
    signal input modulus[k];
    signal input padded_message[k];

    // Check that the signature is in proper form and reduced mod modulus.
    component signatureRangeCheck[k];
    component bigLessThan = BigLessThan(n, k);
    for (var i = 0; i < k; i++) {
        signatureRangeCheck[i] = Num2Bits(n);
        signatureRangeCheck[i].in <== signature[i];
        bigLessThan.a[i] <== signature[i];
        bigLessThan.b[i] <== modulus[i];
    }
    bigLessThan.out === 1;

    component bigPow = FpPow65537Mod(n, k);
    for (var i = 0; i < k; i++) {
        bigPow.base[i] <== signature[i];
        bigPow.modulus[i] <== modulus[i];
    }

    log("out");
    for (var i=0; i < k; i++) {
        log(bigPow.out[i], ",");
    }
    for (var i = 0; i < k; i++) {
        bigPow.out[i] === padded_message[i];
    }
}

template MyRSAVerify65537Test() {
    signal input signature[32];
    signal input modulus[32];
    signal input padded_message[32];

    component verify = MyRSAVerify65537(16, 32);
    for (var i = 0; i < 32; i++) {
        verify.signature[i] <== signature[i];
        verify.modulus[i] <== modulus[i];
        verify.padded_message[i] <== padded_message[i];
    }
}


template FpPow65537ModTest() {
    signal input base[32];
    signal input modulus[32];
    
    component pow = FpPow65537Mod(16, 32);
    for(var i=0; i<32; i++) {
        pow.base[i] <== base[i];
        pow.modulus[i] <== modulus[i];
    }

    for(var i=0; i<32; i++) {
        log("out", i, pow.out[i]);
    }
}

template MySha256Test() {

    signal input input_bits[98];
    component hash = Sha256(98);

    for(var i=0; i<98; i++) {
        hash.in[i] <== input_bits[i];
    }

    for(var i=0; i<256; i++) {
        log(hash.out[i]);
    }
}
// Note: something is wrong with how we are converting hexes to ints
// Maybe they are not in the right order.
component main = MySha256Test();