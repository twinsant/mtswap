# influx.py
import time
from helper import DeFiContract
from web3 import Web3
from tsdb import InfluxDB

ETH_USDT=Web3.toChecksumAddress('0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852')
contract = DeFiContract(ETH_USDT, 'Pair')

db = InfluxDB()

def get_decimal(address):
    token = DeFiContract(address, 'ERC20')
    return token.decimals()

while True:
    r0, r1, _ = contract.getReserves()

    token0_address = contract.token0()
    decimals = get_decimal(token0_address)
    r0 = r0/(10**decimals)

    token1_address = contract.token1()
    decimals = get_decimal(token1_address)
    r1 = r1/(10**decimals)

    print('{} {} {}'.format(ETH_USDT, r0, r1))
    doc = {
        'address': ETH_USDT,
        'r0': r0,
        'r1': r1,
    }
    db.save(doc)
    time.sleep(60)
