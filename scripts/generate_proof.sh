# Calculate the witness
cd circuit_js
node generate_witness.js circuit.wasm ../input.json ../witness.wtns
# Create the proof
cd ../
./node_modules/.bin/snarkjs plonk prove circuit_final.zkey witness.wtns proof.json public.json
# Remove intermediate files
rm witness.wtns
