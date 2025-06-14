// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    string public storedData;

    event DataChanged(string oldValue, string newValue, address indexed changer);

    constructor() {
        storedData = "Initial Value";
    }

    function set(string memory newValue) public {
        string memory oldValue = storedData;
        storedData = newValue;
        emit DataChanged(oldValue, newValue, msg.sender);
    }

    function get() public view returns (string memory) {
        return storedData;
    }
    
}