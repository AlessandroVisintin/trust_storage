// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TreeHashManager {
    bool private locked;

    modifier noReentrancy() {
        require(!locked, "No reentrancy");
        locked = true;
        _;
        locked = false;
    }

    struct Node {
        uint256 parentId;
        address owner;
        bytes32 hash;
        uint256 indexInParent;
    }

    mapping(uint256 => Node) private nodes;
    mapping(uint256 => uint256[]) private childrenOf;
    mapping(bytes32 => uint256) public hashToNodeId;
    uint256 private currentNodeId = 2; // Starts at 2 (root is 1)

    event NodeAdded(uint256 indexed nodeId, uint256 indexed parentId, address indexed owner, bytes32 hash);
    event HashUpdated(uint256 indexed nodeId, bytes32 oldHash, bytes32 newHash, address indexed updater);
    event OwnershipTransferred(uint256 indexed nodeId, address indexed previousOwner, address indexed newOwner);
    event NodeDeprecated(uint256 indexed nodeId, address indexed deprecator);

    constructor() {
        nodes[1] = Node({parentId: 0, owner: msg.sender, hash: bytes32(0), indexInParent: 0});
    }

    function addNode(uint256 parentId, bytes32 hash) external noReentrancy {
        require(hash != bytes32(0), "Invalid hash");
        require(hashToNodeId[hash] == 0, "Hash already exists");
        require(parentId < currentNodeId, "Invalid parent");
        require(nodes[parentId].owner != address(0), "Parent not found");
        if (parentId != 1) {
            require(_isAuthorized(parentId, msg.sender), "Not authorized");
        }

        uint256 newId = currentNodeId++;
        uint256 indexInParent = childrenOf[parentId].length;
        nodes[newId] = Node({parentId: parentId, owner: msg.sender, hash: hash, indexInParent: indexInParent});
        hashToNodeId[hash] = newId;
        childrenOf[parentId].push(newId);
        emit NodeAdded(newId, parentId, msg.sender, hash);
    }

    function updateHash(uint256 nodeId, bytes32 newHash) external noReentrancy {
        require(nodes[nodeId].owner != address(0), "Node not found");
        require(_isAuthorized(nodeId, msg.sender), "Not authorized");
        require(newHash != bytes32(0), "Invalid hash");
        require(hashToNodeId[newHash] == 0, "Hash already exists");

        bytes32 oldHash = nodes[nodeId].hash;
        hashToNodeId[newHash] = nodeId;
        delete hashToNodeId[oldHash];
        nodes[nodeId].hash = newHash;
        emit HashUpdated(nodeId, oldHash, newHash, msg.sender);
    }

    function transferOwnership(uint256 nodeId, address newOwner) external noReentrancy {
        require(newOwner != address(0), "Invalid owner");
        require(_isAuthorized(nodeId, msg.sender), "Not authorized");

        nodes[nodeId].owner = newOwner;
        emit OwnershipTransferred(nodeId, msg.sender, newOwner);
    }

    function deprecateNode(uint256 nodeId) external noReentrancy {
        require(nodeId != 1, "Cannot deprecate root");
        require(nodes[nodeId].owner != address(0), "Node not found");
        require(_isAuthorized(nodeId, msg.sender), "Not authorized");
        require(childrenOf[nodeId].length == 0, "Node has children");

        bytes32 oldHash = nodes[nodeId].hash;
        uint256 parentId = nodes[nodeId].parentId;
        if (parentId != 0) {
            uint256[] storage siblings = childrenOf[parentId];
            uint256 index = nodes[nodeId].indexInParent;
            uint256 lastIndex = siblings.length - 1;

            if (index != lastIndex) {
                uint256 lastNodeId = siblings[lastIndex];
                siblings[index] = lastNodeId;
                nodes[lastNodeId].indexInParent = index;
            }
            siblings.pop();
        }

        delete hashToNodeId[oldHash];
        delete nodes[nodeId];
        emit NodeDeprecated(nodeId, msg.sender);
    }

    function _isAuthorized(uint256 nodeId, address caller) private view returns (bool) {
        Node memory current = nodes[nodeId];
        if (current.owner == caller) return true;
        while (current.parentId != 0) {
            current = nodes[current.parentId];
            if (current.owner == caller) return true;
        }
        return false;
    }

    function getNode(uint256 nodeId) external view returns (uint256 parentId, address owner, bytes32 hash) {
        require(nodes[nodeId].owner != address(0));
        Node memory node = nodes[nodeId];
        return (node.parentId, node.owner, node.hash);
    }

    function getChildren(uint256 nodeId) external view returns (uint256[] memory) {
        require(nodes[nodeId].owner != address(0), "Node not found");
        return childrenOf[nodeId];
    }

    function getNodeIdByHash(bytes32 hash) external view returns (uint256) {
        uint256 nodeId = hashToNodeId[hash];
        require(nodeId != 0, "Hash not found");
        return nodeId;
    }
}
