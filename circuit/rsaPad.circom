// https://medium.com/@bn121rajesh/rsa-sign-and-verify-using-openssl-behind-the-scene-bf3cac0aade2

// 1. hash value (20 byte in case of SHA1) is extended to RSA key size by prefixing padding.
// 2. Default padding scheme in openssl is PKCS1.
// 3. PKCS#1v1.5 padding scheme: 00||01||PS||00||T||H
// 4. PS: Octet string with FF such that length of message is equal to key size.
// 5. T: Identifier of signature scheme (Each scheme has its MAGIC bytes).
// 6. H: Hash value of the message.


template RSAPad(n, k) {
    signal input modulus[k];
    signal input base_message[k];
    signal output padded_message[k];
    signal padded_message_bits[n*k];

    // Note: Padding isn't an essential step 
    // and doesn't add alot to security of our MVP.
    // Hence we could just skip padding and compare the output to last
    // 20 bytes (SHA1-digest)

    // component modulus_n2b[k];
    // component base_message_n2b[k];
    // signal modulus_bits[n*k];
    // signal base_message_bits[n*k];
    // for (var i = 0; i < k; i++) {
    //     base_message_n2b[i] = Num2Bits(n);
    //     base_message_n2b[i].in <== base_message[i];
    //     for (var j = 0; j < n; j++) {
    //         base_message_bits[i*n+j] <== base_message_n2b[i].out[j];
    //     }
    //     modulus_n2b[i] = Num2Bits(n);
    //     modulus_n2b[i].in <== modulus[i];
    //     for (var j = 0; j < n; j++) {
    //         modulus_bits[i*n+j] <== modulus_n2b[i].out[j];
    //     }
    // }

    // for (var i = base_len; i < n*k; i++) {
    //     base_message_bits[i] === 0;
    // }

    // for (var i = 0; i < base_len + 8; i++) {
    //     padded_message_bits[i] <== base_message_bits[i];
    // }
    // component modulus_zero[(n*k + 7 - (base_len + 8))\8];
    // {
    //     var modulus_prefix = 0;
    //     for (var i = n*k - 1; i >= base_len + 8; i--) {
    //         if (i+8 < n*k) {
    //             modulus_prefix += modulus_bits[i+8];
    //             if (i % 8 == 0) {
    //                 var idx = (i - (base_len + 8)) / 8;
    //                 modulus_zero[idx] = IsZero();
    //                 modulus_zero[idx].in <== modulus_prefix;
    //                 padded_message_bits[i] <== 1-modulus_zero[idx].out;
    //             } else {
    //                 padded_message_bits[i] <== padded_message_bits[i+1];
    //             }
    //         } else {
    //             padded_message_bits[i] <== 0;
    //         }
    //     }
    // }
    // // The RFC guarantees at least 8 octets of 0xff padding.
    // assert(base_len + 8 + 65 <= n*k);
    // for (var i = base_len + 8; i < base_len + 8 + 65; i++) {
    //     padded_message_bits[i] === 1;
    // }

    // component padded_message_b2n[k];
    // for (var i = 0; i < k; i++) {
    //     padded_message_b2n[i] = Bits2Num(n);
    //     for (var j = 0; j < n; j++) {
    //         padded_message_b2n[i].in[j] <== padded_message_bits[i*n+j];
    //     }
    //     padded_message[i] <== padded_message_b2n[i].out;
    // }
}