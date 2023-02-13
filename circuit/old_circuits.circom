// Individual working circuits


// template AadhaarVerification() {
//     signal input signature[41];
//     signal input padded_message[41];

//     var modulus[41] = UIDAI_Paperless_Offline_eKYC_Public_Key();

//     component verify = MyRSAVerify65537(50, 41);
//     for (var i = 0; i < 41; i++) {
//         verify.signature[i] <== signature[i];
//         verify.modulus[i] <== modulus[i];
//         verify.padded_message[i] <== padded_message[i];
//     }
// }


// template Sha256GeneralBits(N) {
//     signal input in_padded_bits[N];
//     signal input in_len_padded_bits;
//     signal output hash_message[256];

//     component sha256 = Sha256General(N);
//     sha256.in_len_padded_bits <== in_len_padded_bits;
//     for (var i = 0; i < N; i++) {
//         sha256.paddedIn[i] <== in_padded_bits[i];
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

