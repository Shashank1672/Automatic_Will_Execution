from web3 import Web3
import sys
import pickle
from hexbytes import HexBytes
import json

abi_file, bin_file = sys.argv[1], sys.argv[2]

#Functoin to create the receipt of the deployed smart contract
def createReceipt(txn_receipt):
    my_receipt = {
        'from': txn_receipt['from'],
        'to' : txn_receipt['to'],
        'contractAddress': txn_receipt['contractAddress'],
        'transactionHash': HexBytes.hex(txn_hash)
    }
    with open('contractReceipt.json', 'w') as f:
        json.dump(my_receipt, f)

#Retrive the data from the .bin and .abi file created by the compiler
with open(bin_file, 'rb') as f:
    contract_bytecode = pickle.loads(f.read())
    
with open(abi_file, 'rb') as f:
    contract_abi = pickle.loads(f.read())

# Connect to the local blockchain using Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

#Deploying the smart contract on ganache
#The smart contract deployer is considerd as the Medical Officer
deploy_contract = w3.eth.contract(abi = contract_abi, bytecode = contract_bytecode)
txn_hash = deploy_contract.constructor().transact({'from': w3.eth.accounts[0]})
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
createReceipt(txn_receipt)

print("Smart contract has been successfully deployed in local ethereum blockchain.\nCheck 'contractReceipt.json' for more info.")