// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    string public storedData;
    constructor() { storedData = "Initial Value"; }
    function set(string memory newValue) public { storedData = newValue; }
    function get() public view returns (string memory) { return storedData; }
    function destroy() public { selfdestruct(payable(msg.sender)); }
}