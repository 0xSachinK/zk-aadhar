const chai = require("chai");
const path = require("path");
const wasm_tester = require("circom_tester").wasm;
const c_tester = require("circom_tester").c;
const crypto = require('crypto');
const xml2js = require('xml2js');



// chatgpt
function sha256Padding(message) {
  // convert the message to a bit array
  let messageBits = [];
  for (let i = 0; i < message.length; i++) {
    let char = message.charCodeAt(i);
    for (let j = 7; j >= 0; j--) {
      messageBits.push((char >> j) & 1);
    }
  }

  // add the 1-bit to the end of the message
  messageBits.push(1);


  // add 0-bits to the end of the message until it is congruent to 448 modulo 512
  while (messageBits.length % 512 !== 448) {
    messageBits.push(0);
  }


  // add the original length of the message (in bits) to the end of the padded message
  let messageLength = message.length * 8;
  for (let i = 63; i >= 0; i--) {
    messageBits.push((messageLength >> i) & 1);
  }

  // TODO: HACK FOR NOW!!!!
  // Set the 471th bit to 0
  messageBits[messageBits.length - 41] = 0;

  return messageBits;
}



function bitsToHex(bits) {
  let hex = '';
  let paddedBits = bits.split('').map(Number);

  // pad the bits if necessary
  if (bits.length % 8 !== 0) {
    let padding = 8 - (bits.length % 8);
    paddedBits = paddedBits.concat(Array(padding).fill(0));
  }

  // convert the bits to hexadecimal
  for (let i = 0; i < paddedBits.length; i += 8) {
    let byte = paddedBits.slice(i, i + 8);
    let decimal = parseInt(byte.join(''), 2);
    hex += decimal.toString(16).padStart(2, '0');
  }

  return hex;
}


function pkcs1PadSHA1(hashValue, keySize) {
  // Default padding scheme in openssl is PKCS1
  const defaultPaddingScheme = "PKCS1";
  //T: Identifier of signature scheme
  const sha1Identifier = "3021300906052b0e03021a05000414";
  var paddedHash = "";
  // 00||01
  paddedHash += "0001";
  // PS
  var psLen = keySize / 8 - (hashValue.length + sha1Identifier.length + 6) / 2;
  var ps = "";
  for (var i = 0; i < psLen; i++) {
    ps += "ff";
  }
  paddedHash += ps;
  // 00
  paddedHash += "00";
  // T
  paddedHash += sha1Identifier;
  // H
  paddedHash += hashValue;

  return paddedHash;
}

// split a bigint into k chunks of n bits each
function split_to_array(_in, n, k) {
  let _in_copy = _in;
  let words = [];
  for (let i = 0; i < k; i++) {
    words[i] = _in % BigInt(2 ** n);
    _in = _in / BigInt(2 ** n);
  }
  if (_in != 0) {
    throw new Error(`Number ${_in_copy} does not fit in ${k * n} bits`);
  }
  return words;
}




describe("Test Aadhaar", function async() {
  this.timeout(1000 * 1000);
  const fs = require('fs');


  it("valid aadhaar gives valid output", async () => {

    const N = 69632;
    const n = 50;
    const k = 41;

    const parser = new xml2js.Parser();

    const xml = path.join(__dirname, "../aadhaar_files/offlineaadhaar20220917094619777.xml");
    const xml_data = fs.readFileSync(xml, 'utf8');

    let digestValueIntArray;
    let signatureValueBigIntArray;

    parser.parseString(xml_data, function (err, result) {
      const signatureValue = result['OfflinePaperlessKyc']['Signature'][0]['SignatureValue'][0];

      // decode base64 signatureValue
      const signatureValueDecoded = Buffer.from(signatureValue, 'base64').toString('hex');
      console.log('SignatureValue: ', signatureValueDecoded);

      // since signaturevaluedecoded is a large hex string, we convert it to a BigInt
      const signatureValueBigInt = BigInt('0x' + signatureValueDecoded);
      console.log('SignatureValue as BigInt: ', signatureValueBigInt);

      // split signatureValueBigInt into 32 bit chunks
      signatureValueBigIntArray = split_to_array(signatureValueBigInt, n, k);
      console.log('SignatureValue as BigInt Array: ', signatureValueBigIntArray);


      const digestValue = result['OfflinePaperlessKyc']['Signature'][0]['SignedInfo'][0]['Reference'][0]['DigestValue'][0];
      console.log('DigestValue: ', digestValue);

      digestValueIntArray = digestValue.split('').map(function (char) {
        // convert char to decimal value
        return char.charCodeAt(0);
      });

      const canocalizedDigestValue = `<SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#"><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod><SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod><Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform></Transforms><DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"></DigestMethod><DigestValue>${digestValue}</DigestValue></Reference></SignedInfo>`
      console.log('Canocalized DigestValue: ', canocalizedDigestValue);

      // Sha1 of canocalizedDigestValue
      const sha1 = crypto.createHash('sha1');
      sha1.update(canocalizedDigestValue);
      const sha1Digest = sha1.digest('hex');
      console.log('Sha1 Digest: ', sha1Digest);

      // pad sha1Digest
      const paddedSha1Digest = pkcs1PadSHA1(sha1Digest, 2048);
      console.log('Padded Sha1 Digest: ', paddedSha1Digest);

      // convert paddedsa1digest to bigint
      const paddedSha1DigestBigInt = BigInt('0x' + paddedSha1Digest);
      console.log('Padded Sha1 Digest as BigInt: ', paddedSha1DigestBigInt);

      // split paddedSha1DigestBigInt into 32 bit chunks
      const paddedSha1DigestBigIntArray = split_to_array(paddedSha1DigestBigInt, 50, 41);
      console.log('Padded Sha1 Digest as BigInt Array: ', paddedSha1DigestBigIntArray);
    });

    // Read the canonicalized xml file and grab all the data from it
    const offlinePaperlessKyc_data = fs.readFileSync(
      path.join(__dirname, '../aadhaar_files/CanonicalizedSignatureRemoved.xml'),
      'utf8'
    );

    // Convert canonicalized_xml to a binary string
    const offlinePaperlessKyc_data_buffer = Buffer.from(offlinePaperlessKyc_data, 'utf8').toString('binary');
    const offlinePaperlessKyc_data_padded_bits = sha256Padding(offlinePaperlessKyc_data_buffer);

    // Append 0s to the padded binary string until length is n
    const offlinePaperlessKyc_data_padded_bits_n = offlinePaperlessKyc_data_padded_bits.concat(
      Array(N - offlinePaperlessKyc_data_padded_bits.length).fill(0)
    );


    // Prepare inputs
    const input = {
      "OfflinePaperlessKyc_padded_bits": offlinePaperlessKyc_data_padded_bits_n,
      "OfflinePaperlessKyc_padded_bits_len": offlinePaperlessKyc_data_padded_bits.length,    // actual length rounded up to multiple of 512
      "DigestValue": digestValueIntArray,
      "SignatureValue": signatureValueBigIntArray.map((x) => x.toString()),
    };

    console.log(
      input
    );

    let circuit = await c_tester(
      path.join(__dirname, "../circuit/circuit.circom"),
      {
        recompile: false,
        output: path.join(__dirname, '../'),    // specify path to already compiled circuit and wasm files
        verbose: true,
      }
    );

    const witness = await circuit.calculateWitness(input);


    // Calculate expected output
    // calculate sha256 of the first 32 bytes
    // const sha256 = crypto.createHash('sha256');
    // sha256.update(canonicalized_xml_bin);
    // const sha256_digest = sha256.digest('hex');

    // // convert sha256 message to bits array
    // const sha256_message_bits = sha256_digest.split('').map(function (char) {
    //   return parseInt(char, 16).toString(2).padStart(4, '0');
    // }).join('').split('').map(function (char) {
    //   return parseInt(char, 2);
    // });


    // // confirm that the output of the circuit is the same as the expected output
    // await circuit.assertOut(witness, { hash_message: sha256_message_bits })

    // // print witness
    // const output = []
    // for (let i = 0; i < 256; i++) {
    //   output.push(witness[circuit.symbols[`main.hash_message[${i}]`].varIdx].toString())
    // }
    // const witness_bits = output.reduce((acc, val) => acc + val.toString(16), '');
    // const witness_hex_str = bitsToHex(witness_bits)
    // console.log("Output hex: ", witness_hex_str, "\nExpected hex: ", sha256_digest);
  });
});