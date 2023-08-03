// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FundTransfer {

    //Creating a DATA STRUCTURE for the wills that are being created.
    struct LegalFile {
        address WillMaker;
        address payable receiver;
        uint256 asset;
    }

    //Variable declarations for the contract
    uint256 depo_amount = 0;                 //Amount deposited to the contract 
    address doctor;                     //Wallet address of the one who deploys the above smart contract
    mapping (address => bool) corpse_address;     //Data structure to store the corpse address
    LegalFile [] legalfile;               //Data structue to store the created wills.
    
    /*
        Constructor of the contract.
        Initialise the doctor address to the contract deployer address.
        And the doctor is made not to create any will.
    */
    constructor (){
        doctor = msg.sender;
        corpse_address[msg.sender] = true;
    }

    //Function to create a Will
    function createWill(address payable _addrs) public payable{
        bool dead = (corpse_address[msg.sender]);

        require(!dead, "The Person is considered Dead. Cannot create a Will at this moment.");
        require(msg.value > 0, "Cannot create a Will with ZERO payable.");
        require(msg.sender != _addrs, "Cannot create a Will to the same account.");

        //Creating an instance of the above data structure defined
        LegalFile memory n = LegalFile(
            {
                WillMaker: msg.sender,
                receiver: _addrs,
                asset: msg.value
            }
        );

        corpse_address[msg.sender] = false;
        
        //Appending the Legal file to the data struture and incrementing the depository amount.
        legalfile.push(n);
        depo_amount+=msg.value;
    }


    // Function used by the medical officer to certify the death of the person
    function certify_dead(address _corpse) public {
        require(msg.sender == doctor, "Only Medical Officer can approve the death of a person.");
        corpse_address[_corpse] = true;

        uint i = 0;
        while(i<legalfile.length){
            if (legalfile[i].WillMaker == _corpse){
                address payable nominee = legalfile[i].receiver;
                uint256 amount = legalfile[i].asset;
                
                // Transferring the amount to te nominee by the smart contract and decrementing the depo amount
                nominee.transfer(amount);
                depo_amount-=amount;
                
                //Removing the Legal file from the data structure
                remove_contract(i);
            }
            else
                i++;
        }
    }
    
    //Function to remove the LegalFile instance from the data structure they have been processed
    function remove_contract(uint index) internal {
        require(index < legalfile.length);
        legalfile[index] = legalfile[legalfile.length-1];
        legalfile.pop();
    }

    //Function to get all the pending LegalFiles in the data structure that are not processed yet.
    function getLegalFiles() public view returns (LegalFile []  memory){
        return legalfile;
    }

    //Function to check whether the entered person is dead or not
    function isDead(address _person) public view returns (bool){
        return corpse_address[_person];
    }

    //Function to retrieve the balance amount in the smart contract
    function getContractBalance() public view returns (uint256){
        return depo_amount;
    }
}