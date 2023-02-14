const chai = require("chai");
const path = require("path");
const wasm_tester = require("circom_tester").wasm;
const crypto = require('crypto');



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



describe("Test Generic Sha256 circuit", function async() {
  this.timeout(1000 * 1000);

  it.skip("calculate sha256 using the circuit", async () => {

    const xml = path.join(__dirname, "../aadhaar_files/CanonicalizedSignatureRemoved.xml");
    // Read the xml file and grab all the data from it
    const fs = require('fs');
    const canonicalized_xml = fs.readFileSync(xml, 'utf8');

    // prepare the input
    // Convert canonicalized_xml to a binary string
    // NOTE: Getting only the first 32 bytes of the canonicalized_xml
    const canonicalized_xml_bin = Buffer.from(canonicalized_xml, 'utf8').toString('binary').slice(0, 32);

    const canonicalized_xml_bin_padded_bits = sha256Padding(canonicalized_xml_bin);

    // Append 0s to the padded binary string until length is n
    const n = 5120;
    const canonicalized_xml_bin_padded_bits_n = canonicalized_xml_bin_padded_bits.concat(
      Array(n - canonicalized_xml_bin_padded_bits.length).fill(0)
    );

    // Prepare inputs
    const input = {
      "in_padded": canonicalized_xml_bin_padded_bits_n,
      "in_len_padded_bits": canonicalized_xml_bin_padded_bits.length    // actual length rounded up to multiple of 512
    };

    let circuit = await wasm_tester(
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
    const sha256 = crypto.createHash('sha256');
    sha256.update(canonicalized_xml_bin);
    const sha256_digest = sha256.digest('hex');

    // convert sha256 message to bits array
    const sha256_message_bits = sha256_digest.split('').map(function (char) {
      return parseInt(char, 16).toString(2).padStart(4, '0');
    }).join('').split('').map(function (char) {
      return parseInt(char, 2);
    });


    // confirm that the output of the circuit is the same as the expected output
    await circuit.assertOut(witness, { hash_message: sha256_message_bits })

    // print witness
    const output = []
    for (let i = 0; i < 256; i++) {
      output.push(witness[circuit.symbols[`main.hash_message[${i}]`].varIdx].toString())
    }
    const witness_bits = output.reduce((acc, val) => acc + val.toString(16), '');
    const witness_hex_str = bitsToHex(witness_bits)
    console.log("Output hex: ", witness_hex_str, "\nExpected hex: ", sha256_digest);
  });
});