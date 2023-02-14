pragma circom 2.1.0;

include "../node_modules/circomlib/circuits/bitify.circom";
include "../node_modules/circomlib/circuits/sha256/sha256.circom";

include "../zk-email-verify-circuits/fp.circom";
include "../zk-email-verify-circuits/rsa.circom";
include "../zk-email-verify-circuits/base64.circom";
include "../zk-email-verify-circuits/sha256general.circom";

include "./public_key.circom";
include "../sha1-circuits/sha1.circom";


// 
//  Calculates the Sha256 of `in_bytes` and returns the result in `out[256]`. 
//
template Sha256Bytes(N) {
    signal input in_bytes[N];
    signal output out_bits[256];

    component bitifier[N];
    for (var i = 0; i < N; i++) {
        bitifier[i] = Num2Bits(8);
        bitifier[i].in <== in_bytes[i];
    }

    component hasher = Sha256(8 * N);
    for (var i = 0; i < N; i++) {
        for (var j = 0; j < 8; j++) {
            hasher.in[i * 8 + j] <== bitifier[i].out[7 - j];
        }
    }

    for (var i = 0; i < 256; i++) {
        out_bits[i] <== hasher.out[i];
    }
}


//
// Calculates the Sha1 of `in_bytes` and returns the result in `out_bits[160]`.
//
template Sha1Bytes(N) {
    signal input in_bytes[N];
    signal output out_bits[160];

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

    // Need to modify the out slightly to get the actual sha1 value.
    // out = []
    // for i in range(5):
    //    out += out_bits[i * 32 : (i + 1) * 32][::-1]
    // print(hex(int(''.join(out), 2)))

    for (var i = 0; i < 5; i++) {
        for (var j = 0; j < 32; j++) {
            out_bits[i * 32 + j] <== hasher.out[i * 32 + 31 - j];
        }
    }   
}


//
// Verifies RSA signatures with exponent 65537.
//
template RSASignatureVerify(n, k) {
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


template Pkcs1v1_5_SHA1_Padding(out_bits_len) {
    signal input in_bits[160];

    var asn1_bits[120] = Pkcs1v1_5_Padding_ASN1_SHA1_Bits();

    signal output out_bits[out_bits_len + 2];

    out_bits[0] <== 0;
    out_bits[1] <== 0;

    // 00
    for (var i = 2; i < 10; i++) {
        out_bits[i] <== 0;
    }

    // 01
    for (var i = 10; i < 17; i++) {
        out_bits[i] <== 0;
    }
    out_bits[17] <== 1;

    // ff
    var ff_octet_str_length = out_bits_len - (
        160     // sha1 bits
        + 120   // asn1 bits
        + 24    // 00, 01, 00 bits
    );
    for (var i = 18; i < ff_octet_str_length + 18; i++) {
        out_bits[i] <== 1;
    }

    // 00
    for (var i = ff_octet_str_length + 18; i < ff_octet_str_length + 26; i++) {
        out_bits[i] <== 0;
    }

    // asn1
    for (var i = ff_octet_str_length + 26; i < ff_octet_str_length + 146; i++) {
        out_bits[i] <== asn1_bits[i - ff_octet_str_length - 26];
    }

    // sha1
    for (var i = ff_octet_str_length + 146; i < out_bits_len + 2; i++) {
        out_bits[i] <== in_bits[i - ff_octet_str_length - 146];
    }

    // Note: out_bits is packed from the left, so the first bit is the most significant bit.
}



template Aadhaar(N) {

    // 
    // Phase 1: Verify the hash of the OfflinePaperlessKyc element matches the DigestValue
    //

    // Bits of the OfflinePaperlessKyc element, padded to the nearest multiple of 512 and then padded with additional zeroes
    signal input OfflinePaperlessKyc_padded_bits[N];
    signal input OfflinePaperlessKyc_padded_bits_len;
    signal input DigestValue[44];
    signal input signature[41];     // 41 chunks of 50 bytes

    
    // Calculate Sha256 of OfflinePaperlessKyc element
    component sha256 = Sha256General(N);
    sha256.in_len_padded_bits <== OfflinePaperlessKyc_padded_bits_len;
    for (var i = 0; i < N; i++) {
        sha256.paddedIn[i] <== OfflinePaperlessKyc_padded_bits[i];
    }
    
    // Calculate Base64 decoding of the DigestValue
    component base64_decoder = Base64Decode(33);
    for (var i = 0; i < 44; i++) {
        base64_decoder.in[i] <== DigestValue[i];
    }

    // Convert the 32 bytes of the Base64 decoded DigestValue to bits
    component bitifier[32];
    signal base64_decoded_bits[256];
    for (var i = 0; i < 32; i++) {
        bitifier[i] = Num2Bits(8);
        bitifier[i].in <== base64_decoder.out[i];
        for (var j = 0; j < 8; j++) {
            base64_decoded_bits[i * 8 + j] <== bitifier[i].out[7 - j];
        }
    }

    // Log the two values for debugging
    for (var i = 0; i < 256; i++) {
        log("sha256.out[", i, "] = ", sha256.out[i]);
    }
    for (var i = 0; i < 256; i++) {
        log("base64_decoded_bits[", i, "] = ", base64_decoded_bits[i]);
    }

    // Compare the two and ensure they are equal
    for (var i = 0; i < 256; i++) {
        sha256.out[i] === base64_decoded_bits[i];
    }

    //
    // Phase 2: Prepare the base message to be fed into the RSA signature verification
    //

    var signed_info_element_bytes_var[563] = Canonicalized_Signed_Info_Element();
    signal signed_info_element_bytes[563];

    // Todo: How safe is this? Can it be modified by a malicious prover?
    for (var i = 0; i < 480; i++) {
        signed_info_element_bytes[i] <== signed_info_element_bytes_var[i];
    }
    // Inject the digest value int the canonicalized signed info element
    for (var i = 480; i < 480 + 44; i++) {
        signed_info_element_bytes[i] <== DigestValue[i - 480];
    }
    for (var i = 480 + 44; i < 563; i++) {
        signed_info_element_bytes[i] <== signed_info_element_bytes_var[i];
    }

    // Calculate sha1 of the signed info element
    component sha1 = Sha1Bytes(563);
    for (var i = 0; i < 563; i++) {
        sha1.in_bytes[i] <== signed_info_element_bytes[i];
    }

    // Pad the sha1 output using the PKCS#1 v1.5 padding scheme
    component sha1_padder = Pkcs1v1_5_SHA1_Padding(2048);
    for (var i = 0; i < 160; i++) {
        sha1_padder.in_bits[i] <== sha1.out_bits[i];
    }

    // Create base message out of the padded sha1 output
    component bits2Num[41];
    for (var i = 0; i < 41; i++) {
        bits2Num[i] = Bits2Num(50);
        for (var j = 0; j < 50; j++) {
            bits2Num[i].in[j] <== sha1_padder.out_bits[2049 - i * 50 - j];
        }
    }

    //
    // Phase 3: Verify the RSA signature
    //
    component sigVerifier = RSASignatureVerify(50, 41);
    var modulus[41] = UIDAI_Paperless_Offline_eKYC_Public_Key();

    for (var i = 0; i < 41; i++) {
        sigVerifier.signature[i] <== signature[i];
        sigVerifier.modulus[i] <== modulus[i];
        sigVerifier.padded_message[i] <== bits2Num[i].out;
    }
}

// 67,032 bits (8,379 chars) are present in my Aadhaar XML file
// Add 3% to that and round up to the nearest multiple of 512
// 69,632 bits (~9k chars) is the number of max bits we should need. 
// (Yeah, I chose 3% to make it a nice number with 69 in it.)

component main = Aadhaar(69632);