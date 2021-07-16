# DeFi Helper
import json
import os
from web3 import Web3

class ContractCall():
    def __init__(self, method_to_call):
        self.method_to_call = method_to_call

    def __call__(self, *args, **kwargs):
        return self.method_to_call(*args, **kwargs).call()

class DeFiContract():
    infura_url = 'https://mainnet.infura.io/v3/%s' % os.getenv('INFURA_PROJECT_ID', 'YOUR_INFURA_PROJECT_ID')
    web3 = Web3(Web3.HTTPProvider('http://172.16.0.155:9545'))


    def __getattr__(self, name):
        ret = None
        for i in self.abi:
            if i['type'] == 'function' and name == i['name']:
                method_to_call = getattr(self.contract.functions, name)
                ret = ContractCall(method_to_call)
        return ret

    def __init__(self, contract_address, abi_name, chain='eth'):
        if chain == 'bsc':
            self.web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
        fn = os.path.join(os.path.dirname(__file__), 'IUniswapV2{}.json'.format(abi_name))
        with open(fn) as f:
            c = f.read()
        self.abi = json.loads(c)['abi']
        self.contract = self.web3.eth.contract(address=contract_address, abi=self.abi)