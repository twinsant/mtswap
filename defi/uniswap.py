from helper import DeFiContract


UNISWAP_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
factory_contract = DeFiContract(UNISWAP_ADDRESS, 'Factory')


#returns a count of all the trading pairs on uniswap
allPairsLength = factory_contract.allPairsLength()
print(allPairsLength)

for i in range(1, 10):
    allPairs_address = factory_contract.allPairs(i)
    pair_contract = DeFiContract(allPairs_address, 'Pair')

    token0_address = pair_contract.token0()
    token0 = DeFiContract(token0_address, 'ERC20')
    symbol0 = token0.symbol()
    decimals0 = token0.decimals()

    token1_address = pair_contract.token1()
    token1 = DeFiContract(token1_address, 'ERC20')
    symbol1 = token1.symbol()
    decimals1 = token1.decimals()

    reserves = pair_contract.getReserves()
    print('{} {:<5} {:<5} {} {} {}'.format(allPairs_address, symbol0, symbol1, reserves, decimals0, decimals1))