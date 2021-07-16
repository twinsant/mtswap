from helper import DeFiContract
from database import MongoDB
import web3


UNISWAP_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
# https://docs.pancakeswap.finance/code/smart-contracts
PANCAKESWAP = '0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73'
factory_contract = DeFiContract(PANCAKESWAP, 'Factory', chain='bsc')


#returns a count of all the trading pairs on uniswap
allPairsLength = factory_contract.allPairsLength()

db = MongoDB('bsc')
syncedPairs = db.getSyncedPairs()

for i in range(syncedPairs + 1, allPairsLength):
    allPairs_address = factory_contract.allPairs(i)
    pair_contract = DeFiContract(allPairs_address, 'Pair', chain='bsc')

    token0_address = pair_contract.token0()
    token0 = DeFiContract(token0_address, 'ERC20', chain='bsc')
    try:
        symbol0 = token0.symbol()
    except OverflowError:
        symbol0 = 'ERROR'
    except web3.exceptions.ContractLogicError:
        symbol0 = 'ERROR'
    except web3.exceptions.BadFunctionCallOutput:
        symbol0 = 'ERROR'

    try:
        decimals0 = token0.decimals()
    except web3.exceptions.ContractLogicError:
        decimals0 = 18
    except web3.exceptions.BadFunctionCallOutput:
        decimals0 = 18

    token1_address = pair_contract.token1()
    token1 = DeFiContract(token1_address, 'ERC20', chain='bsc')
    try:
        symbol1 = token1.symbol()
    except OverflowError:
        symbol1 = 'ERROR'
    except web3.exceptions.ContractLogicError:
        symbol1 = 'ERROR'
    except web3.exceptions.BadFunctionCallOutput:
        symbol1 = 'ERROR'
    try:
        decimals1 = token1.decimals()
    except web3.exceptions.ContractLogicError:
        decimals1 = 18
    except web3.exceptions.BadFunctionCallOutput:
        decimals1 = 18

    reserve0, reserve1, _ = pair_contract.getReserves()
    reserve0 = reserve0 / (10**decimals0)
    reserve1 = reserve1 / (10**decimals1)
    print('{} {} {:<5} {:<5} {:>18.2f} {:>18.2f}'.format(i, allPairs_address, symbol0, symbol1, reserve0, reserve1))
    doc = {
        'idx': i,
        'address': allPairs_address,
        'token0': token0_address,
        'token1': token1_address,
    }
    db.save(doc)