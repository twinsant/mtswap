from web3 import Web3
import asyncio
from helper import DeFiContract

UNISWAP_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
contract = DeFiContract(UNISWAP_ADDRESS, 'Factory')

def handle_event(event):
    print(Web3.toJSON(event))

async def log_loop(event_filter, poll_interval):
    while True:
        for PairCreated in event_filter.get_new_entries():
            handle_event(PairCreated)
        await asyncio.sleep(poll_interval)

def main():
    event_filter = contract.contract.events.PairCreated.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)
            )
        )
    finally:
        loop.close()

if __name__ == '__main__':
    main()