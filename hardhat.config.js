/**
 * @type import('hardhat/config').HardhatUserConfig
 */
require('@nomiclabs/hardhat-ethers');
const { infuraApiKey, mnemonic } = require('./scripts/secrets.json')

module.exports = {
  solidity: "0.6.12",
  networks: {
    ropsten: {
      url: 'https://ropsten.infura.io/v3/projectid',
      accounts: {mnemonic: mnemonic}
    }
  }
};
