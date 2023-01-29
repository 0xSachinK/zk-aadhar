pragma circom 2.1.0;

include "../node_modules/circomlib/circuits/sha256/sha256.circom";

include "../helper-circuits/fp.circom";
include "../helper-circuits/rsa.circom";
include "./public_key.circom";

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

    for (var i = 0; i < k; i++) {
        bigPow.out[i] === padded_message[i];
    }
}


template AadhaarVerification() {
    signal input signature[41];
    signal input padded_message[41];
    signal input uid_data_bytes[1000];

    var modulus[41] = UIDAI_Paperless_Offline_eKYC_Public_Key();

    component verify = MyRSAVerify65537(50, 41);
    for (var i = 0; i < 41; i++) {
        verify.signature[i] <== signature[i];
        verify.modulus[i] <== modulus[i];
        verify.padded_message[i] <== padded_message[i];
    }
}


template AadhaarSha256Verification(N) {
    signal input uid_data_bytes[N];
    signal output hash_message[256];

    component bitifier[N];
    for (var i = 0; i < N; i++) {
        bitifier[i] = Num2Bits(8);
        bitifier[i].in <== uid_data_bytes[i];
    }

    component hasher = Sha256(8 * N);
    for (var i = 0; i < N; i++) {
        for (var j = 0; j < 8; j++) {
            hasher.in[i * 8 + j] <== bitifier[i].out[7 - j];
        }
    }

    for (var i = 0; i < 256; i++) {
        hash_message[i] <== hasher.out[i];
    }
}


component main = AadhaarSha256Verification(8379);
