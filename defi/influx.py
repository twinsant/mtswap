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

    print('{} {} {}'.format(pair, r0, r1))
    doc = {
        'address': pair,
        'r0': r0,
        'r1': r1,
        't': datetime.utcnow().timestamp(),
    }
    return doc

while True:
    all_pairs = m.get_all_pairs()

    now = datetime.now().timestamp()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for pair in all_pairs:
            futures.append(executor.submit(scrapReserves, pair))
        for future in concurrent.futures.as_completed(futures):
            doc = future.result()
            # k.save(doc)
    elapsed = datetime.now().timestamp() - now
    print('Sleeping after {}s...'.format(elapsed))
    time.sleep(60)
