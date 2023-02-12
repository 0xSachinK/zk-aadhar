// Write code to extract SignaturValue and DigestValue from the XML file

const fs = require('fs');
const xml2js = require('xml2js');
const crypto = require('crypto');



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


function prepareInputForRSAVerificationCircuit(xml) {

  const parser = new xml2js.Parser();
  // const xml = fs.readFileSync('./node_scripts/offlineaadhaar20220917094619777.xml', 'utf8');


  parser.parseString(xml, function (err, result) {
    const signatureValue = result['OfflinePaperlessKyc']['Signature'][0]['SignatureValue'][0];

    // decode base64 signatureValue
    const signatureValueDecoded = Buffer.from(signatureValue, 'base64').toString('hex');
    console.log('SignatureValue: ', signatureValueDecoded);

    // since signaturevaluedecoded is a large hex string, we convert it to a BigInt
    const signatureValueBigInt = BigInt('0x' + signatureValueDecoded);
    console.log('SignatureValue as BigInt: ', signatureValueBigInt);

    // split signatureValueBigInt into 32 bit chunks
    const signatureValueBigIntArray = split_to_array(signatureValueBigInt, 50, 41);
    console.log('SignatureValue as BigInt Array: ', signatureValueBigIntArray);


    const digestValue = result['OfflinePaperlessKyc']['Signature'][0]['SignedInfo'][0]['Reference'][0]['DigestValue'][0];
    console.log('DigestValue: ', digestValue);

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

    // create a json file called input.json and write signatureValueBigIntArray and paddedSha1DigestBigIntArray to it
    const input = {
      signature: signatureValueBigIntArray.map(x => x.toString()),
      padded_message: paddedSha1DigestBigIntArray.map(x => x.toString())
    }
    fs.writeFileSync('./input.json', JSON.stringify(input));
  });
}
