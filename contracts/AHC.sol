// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/presets/ERC20PresetMinterPauser.sol";

// 0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9
contract AtomicHabitToken is ERC20PresetMinterPauser {
    constructor(uint256 initialSupply) ERC20PresetMinterPauser("Atomic Habit Token", "AHT") public {
        _mint(msg.sender, initialSupply);
    }
}