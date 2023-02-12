pragma circom 2.1.0;

// include "../helper-circuits/fp.circom";
// include "../helper-circuits/rsa.circom";
// include "../zk-email-verify-circuits/sha256general.circom";
// include "../node_modules/circomlib/circuits/sha256/sha256.circom";
// include "./public_key.circom";
// include "../zk-email-verify-circuits/base64.circom";
include "../sha1-circuits/sha1.circom";

// RSA VERIFICATION CIRCUIT
// template MyRSAVerify65537(n, k) {
//     signal input signature[k];
//     signal input modulus[k];
//     signal input padded_message[k];

//     // Check that the signature is in proper form and reduced mod modulus.
//     component signatureRangeCheck[k];
//     component bigLessThan = BigLessThan(n, k);
//     for (var i = 0; i < k; i++) {
//         signatureRangeCheck[i] = Num2Bits(n);
//         signatureRangeCheck[i].in <== signature[i];
//         bigLessThan.a[i] <== signature[i];
//         bigLessThan.b[i] <== modulus[i];
//     }
//     bigLessThan.out === 1;

//     component bigPow = FpPow65537Mod(n, k);
//     for (var i = 0; i < k; i++) {
//         bigPow.base[i] <== signature[i];
//         bigPow.modulus[i] <== modulus[i];
//     }

//     for (var i = 0; i < k; i++) {
//         bigPow.out[i] === padded_message[i];
//     }
// }


// RSA VERIFICATION WITH PUB KEY CIRCUIT
// template AadhaarVerification() {
//     signal input signature[41];
//     signal input padded_message[41];
//     signal input uid_data_bytes[1000];

//     var modulus[41] = UIDAI_Paperless_Offline_eKYC_Public_Key();

//     component verify = MyRSAVerify65537(50, 41);
//     for (var i = 0; i < 41; i++) {
//         verify.signature[i] <== signature[i];
//         verify.modulus[i] <== modulus[i];
//         verify.padded_message[i] <== padded_message[i];
//     }
// }

// SHA256 Verification Circuit
// template AadhaarSha256Verification(N) {
//     signal input uid_data_bytes[N];
//     signal output hash_message[256];

//     component bitifier[N];
//     for (var i = 0; i < N; i++) {
//         bitifier[i] = Num2Bits(8);
//         bitifier[i].in <== uid_data_bytes[i];
//     }

//     component hasher = Sha256(8 * N);
//     for (var i = 0; i < N; i++) {
//         for (var j = 0; j < 8; j++) {
//             hasher.in[i * 8 + j] <== bitifier[i].out[7 - j];
//         }
//     }

//     for (var i = 0; i < 256; i++) {
//         hash_message[i] <== hasher.out[i];
//     }
// }

// Sha256General Verification Circuit
// template AadhaarSha256Verification(N) {
//     signal input in_padded[N];
//     signal input in_len_padded_bits;
//     signal output hash_message[256];

//     component sha256 = Sha256General(N);
//     sha256.in_len_padded_bits <== in_len_padded_bits;
//     for (var i = 0; i < N; i++) {
//         sha256.paddedIn[i] <== in_padded[i];
//     }

//     for (var i = 0; i < 256; i++) {
//         hash_message[i] <== sha256.out[i];
//     }
// }


// template MyBase64Decoder() {

//     // in = 44 chars or 44 * 6 = 264 bits
//     // out = 264 / 8 = 33 bytes

//     signal input in[44];
//     signal output out[33];

//     component decoder = Base64Decode(33);

//     for (var i = 0; i < 44; i++) {
//         decoder.in[i] <== in[i];
//     }

//     // Last bit is 0, so could just do the 32 bytes
//     for (var i = 0; i < 33; i++) {
//         out[i] <== decoder.out[i];
//     }

//     for (var i = 0; i < 33; i++) {
//         log(out[i]);
//     }

//     // output matches the output of the python script
// }

template MySha1(N) {


    signal input in_bytes[N];
    signal output hash_message[160];

    component bitifier[N];
    for (var i = 0; i < N; i++) {
        bitifier[i] = Num2Bits(8);
        bitifier[i].in <== in_bytes[i];
    }

    component hasher = Sha1(8 * N);
    for (var i = 0; i < N; i++) {
        for (var j = 0; j < 8; j++) {
            hasher.in[i * 8 + j] <== bitifier[i].out[7 - j];
        }
    }

    for (var i = 0; i < 160; i++) {
        hash_message[i] <== hasher.out[i];
    }

    // Need to modify the out slightly to get the actual sha1 value.
    // out = []
    // for i in range(5):
    //    out += hash_message[i * 32 : (i + 1) * 32][::-1]
    // print(hex(int(''.join(out), 2)))

}

// template AadhaarDigestValueVerification(N) {
//     signal input canonicalized_signed_info[563];        // fixed value for all aadhaar XML files
    
//     var digest_value_start_index = 480;
//     var digest_value_length = 44;

//     component base64_decoder = Base64Decode(N);

//     signal input digest_value[digest_value_length];
//     for (var i = digest_value_start_index; i < digest_value_start_index + digest_value_length; i++) {
//         digest_value[i - digest_value_start_index] <== canonicalized_signed_info[i];
//     }

// }


// 67,032 bits (8,379 chars) are present in my Aadhaar XML file
// Add 10% to that and round up to the nearest multiple of 512
// 73,728 bits (~9k chars) is the number of max bits we should need.

component main = MySha1(563);