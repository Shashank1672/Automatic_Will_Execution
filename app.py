from web3 import Web3
import json
import pickle
import os
import time
from hexbytes import HexBytes

#Read the .abi file and the contract receipt
with open('FundTransfer.abi', 'rb') as f:
    contract_abi = pickle.loads(f.read())

with open('contractReceipt.json') as f:
    txn_receipt = json.load(f)

#Read the home page file
with open("interface.txt") as f:
    home_page = f.read()

#Connect to the local ethereum network
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

#Get the contract address from the reeipt file
#Create an CONTRACT object using the address and abi
contract_address = txn_receipt['contractAddress']
deployed_contract = w3.eth.contract(address = contract_address, abi = contract_abi)


#Function to create will
def py_create_will():
    willMaker = input("\nEnter your wallet address: ")
    nominee = input("Enter your nominee wallet address: ")
    asset = input("Enter the amount (in ETH): ")
    value = w3.to_wei(asset, 'ether')
    
    #Acknowledgement of will creation
    print("\n+++++++++++++++++++++++++++ ACKNOWLEDGEMENT REQUIRED ++++++++++++++++++++++++++++++++++++++")
    print(f"\nYou are creating a WILL for your nominee")
    print(f"Nominee: {nominee}")
    print(f"Asset to transfer: {asset} ETH")
    
    if input("\nPress 1 to confirm and sign the transation: ") == '1':
        #Arguments for Transaction function 
        txn_params = {
            'from': willMaker,
            'value': value,
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
        }
        
        #try-except block to catch errorenous transaction in executing the smart contract
        try:
            txn_hash = deployed_contract.functions.createWill(nominee).transact(txn_params)
            print("\nYour contract has been registered.")
            print("The Transaction hash is: ",HexBytes.hex(txn_hash))
        except Exception as e:
            print(e)
    
    else:
        print("\nYou have cancelled the smart contract execution.")
    
    print("\nYou will redirected to home page.")
    time.sleep(10)


#Function to certify the person as dead.
#In our case the first wallet address (contract Deployer) is considered as DOCTOR.
def py_approve_dead():
    corpse = input("\nEnter the wallet address of the dead person: ")
    print(f"\nYou are trying to declare that the person with the wallet address {corpse} is dead.")
    
    if input("Type 'CONFIRM' to continue: ").lower() == 'confirm':
        txn_params = {
            #Ensured this function can only used by the doctor.
            'from': input("Enter your wallet address: "),
            'gas': 300000,
            'gasPrice': w3.to_wei('50', 'gwei'),
        }
        
        try:
            #In the solidity file, it internally transfers the deposited amount to their nominee
            txn_hash = deployed_contract.functions.certify_dead(corpse).transact(txn_params)
            print(f"\nThe person with wallet address {corpse} is certified dead.")
            print("The Transaction hash is: ",HexBytes.hex(txn_hash))
        except Exception as e:
            print(e)
            
    else:
        print("\nInvalid input. Transaction cancelled.")
        
    print("\nYou will redirected to home page.")
    time.sleep(10)

#Function to get all the wills that are created by the customers
#A will includes WILL MAKER - NOMINEE - ASSET TO BE TRANSFERED
def get_records():
    legal_files = deployed_contract.functions.getLegalFiles().call()
    if len(legal_files) == 0:
        print("\nNo Wills to display\n")
    else:
        for i in legal_files:
            print("Will Maker: ",i[0])
            print("Nominee: ",i[1])
            print("Asset: ",i[2])
            print("\n")
            
    print("You will redirected to home page.")
    time.sleep(20)

#To retrieve the balance of the smart contract
#Smart contract balance means - the total amount that has been deposited by all the clients
def get_balance():
    balance = deployed_contract.functions.getContractBalance().call()
    balance = balance/(10**18)
    print("\nDepository Balance: ",balance," ETH")
    
    print("\nYou will redirected to home page.")
    time.sleep(10)
    
#To check whether the person is dead or alive
#Input - Wallet address of the person
#Output - True -> Person is dead. False -> Person is dead
def is_dead():
    person = input("\nEnter the wallet address: ")
    dead = deployed_contract.functions.isDead(person).call()
    if dead:
        print("The person is DEAD")
    else:
        print("The person is ALIVE")
        
    print("\nYou will redirected to home page.")
    time.sleep(10)


choice = 1
while choice:
    os.system('cls')
    print(home_page)
    choice = input("\nEnter your choice: ")
    
    if choice == '1':
        py_create_will()
    elif choice == '2':
        py_approve_dead()
    elif choice == '3':
        get_records()
    elif choice == '4':
        get_balance()
    elif choice == '5':
        is_dead()
    else:
        print("Invalid Input")