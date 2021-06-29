# influx.py
import time
from datetime import datetime
import concurrent

from helper import DeFiContract
from web3 import Web3
from web3 import exceptions
from kfk import KafkaDB
from database import MongoDB

k = KafkaDB()
m = MongoDB()

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
    return doc

def get_decimal(address):
    token = DeFiContract(address, 'ERC20')
    decimal = 18
    try:
        decimal = token.decimals()
    except exceptions.ContractLogicError:
        pass
    except exceptions.BadFunctionCallOutput:
        pass
    return decimal

while True:
    all_pairs = m.get_all_pairs()

    now = datetime.now().timestamp()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pair in all_pairs:
            futures.append(executor.submit(scrapReserves, pair))
        for future in concurrent.futures.as_completed(futures):
            doc = future.result()
            k.save(doc)
    elapsed = datetime.now().timestamp() - now
    print('Sleeping after {}s...'.format(elapsed))
    time.sleep(60)
