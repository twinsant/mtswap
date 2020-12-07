// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/presets/ERC20PresetMinterPauser.sol";

// 0x5FbDB2315678afecb367f032d93F642f64180aa3
contract AtomicHabitToken is ERC20PresetMinterPauser {
    constructor(uint256 initialSupply) ERC20PresetMinterPauser("Atomic Habit Token", "AHT") public {
        _mint(msg.sender, initialSupply);
    }
}