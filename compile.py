import solcx
import pickle
import sys

#Selecting the solidity compiler version
solcx.set_solc_version('0.8.0')

solidity_file = sys.argv[1][:-4:]

#Read the solidity file source code
with open(solidity_file +'.sol') as f:
    source_code = f.read()

#Compile the .sol file
compiled_sol = solcx.compile_source(source_code)

contract_interface = compiled_sol['<stdin>:'+solidity_file]
contract_bytecode = pickle.dumps(contract_interface['bin'])
contract_abi = pickle.dumps(contract_interface['abi'])

#Write the compiled code .bin and .abi code to the files
with open(solidity_file +'.bin', 'wb') as f:
    f.write(contract_bytecode)

with open(solidity_file +'.abi', 'wb') as f:
    f.write(contract_abi)

print(f"{solidity_file}.sol has been successfully compiled")