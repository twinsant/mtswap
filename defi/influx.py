# influx.py
import time
from datetime import datetime

from helper import DeFiContract
from web3 import Web3
from kfk import KafkaDB

db = KafkaDB()

def scrapReserves(pair_address):
    pair=Web3.toChecksumAddress(pair_address)
    contract = DeFiContract(pair, 'Pair')
    r0, r1, _ = contract.getReserves()

    token0_address = contract.token0()
    decimals = get_decimal(token0_address)
    r0 = r0/(10**decimals)

    token1_address = contract.token1()
    decimals = get_decimal(token1_address)
    r1 = r1/(10**decimals)

    print('{} {} {}'.format(pair, r0, r1))
    doc = {
        'address': pair,
        'r0': r0,
        'r1': r1,
        't': datetime.utcnow().timestamp(),
    }
    db.save(doc)

def get_decimal(address):
    token = DeFiContract(address, 'ERC20')
    return token.decimals()

while True:
    scrapReserves('0x0d4a11d5eeaac28ec3f61d100daf4d40471f1852')
    time.sleep(60)
