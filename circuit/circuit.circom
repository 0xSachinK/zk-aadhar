pragma circom 2.1.0;

include "../helper-circuits/fp.circom";
include "../helper-circuits/rsa.circom";
include "../zk-email-verify-circuits/sha256general.circom";
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


// template AadhaarSha256Verification(N) {
//     signal input in_padded[N];
//     signal input in_len_padded_bytes;
//     signal output hash_message[256];

//     component sha256 = Sha256Bytes(N);
//     sha256.in_len_padded_bytes <== in_len_padded_bytes;
//     for (var i = 0; i < N; i++) {
//         sha256.in_padded[i] <== in_padded[i];
//     }

//     for (var i = 0; i < 256; i++) {
//         hash_message[i] <== sha256.out[i];
//     }
// }

template AadhaarSha256Verification(N) {
    signal input in_padded[N];
    signal input in_len_padded_bits;
    signal output hash_message[256];

    component sha256 = Sha256General(N);
    sha256.in_len_padded_bits <== in_len_padded_bits;
    for (var i = 0; i < N; i++) {
        sha256.paddedIn[i] <== in_padded[i];
    }

    for (var i = 0; i < 256; i++) {
        hash_message[i] <== sha256.out[i];
    }
}


// 10,000 chars (8,379 were present in my Aadhaar XML file)
// 10,000 * 8 = 80,000 bits
// 512 * 157 = 80,384 bits
component main = AadhaarSha256Verification(1024);
