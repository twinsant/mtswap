from web3 import Web3
import asyncio
from helper import DeFiContract
from database import MongoDB

def handle_event(event):
    print(Web3.toJSON(event))

async def log_loop(address, poll_interval):
    contract = DeFiContract(address, 'Pair')
    event_filter = contract.contract.events.Swap.createFilter(fromBlock='latest')
    print('Working at {}...'.format(address))

    while True:
        try:
            print('-> ', address)
            for swap in event_filter.get_new_entries():
                handle_event(swap)
        except ValueError:
            print('ERR: {}'.format(address))
        await asyncio.sleep(poll_interval)

def main():
    m = MongoDB()
    tasks = []

    all_pairs = m.get_all_pairs()

    for address in all_pairs[:100]:
        pair=Web3.toChecksumAddress(address)
        task = log_loop(pair, 60)
        tasks.append(task)
    print('{} Starting...'.format(len(tasks)))

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(*tasks)
        )
    finally:
        loop.close()

if __name__ == '__main__':
    main()