from database import MongoDB
from helper import DeFiContract
from web3 import exceptions

if __name__ == '__main__':
    db = MongoDB()
    tokens = db.get_all_tokens()
    print(len(tokens))
    for token in tokens:
        if db.get_token(token) is None:
            try:
                t = DeFiContract(token, 'ERC20')
                name = t.name()
                symbol = t.symbol()
                decimals = t.decimals()
                print('{} {}({}) {}'.format(token, name, symbol, decimals))
                db.save_token({
                    'address': token,
                    'name': name,
                    'symbol': symbol,
                    'decimals': decimals,
                })
            except OverflowError:
                # https://www.gitmemory.com/issue/blockchain-etl/ethereum-etl/240/796883933
                t = DeFiContract(token, 'ERC20Fixed')
                name = t.name().decode('utf-8')
                symbol = t.symbol().decode('utf-8')
                decimals = t.decimals()
                print('{} {}({}) {}'.format(token, name, symbol, decimals))
                db.save_token({
                    'address': token,
                    'name': name,
                    'symbol': symbol,
                    'decimals': decimals,
                })
            except exceptions.ContractLogicError:
                if token == '0x842022dA959FB6944c144d02A9Cc7B7DBbe478F2':
                    continue
                print(token)
                t = DeFiContract(token, 'ERC20Fixed2')
                if token == '0x1f0d3048b3D49DE0ed6169A443dBB049e6DaA6CE':
                    name = 'BET99'
                    symbol = 'BET99'
                elif token in [
                    '0xEB9951021698B42e4399f9cBb6267Aa35F82D59D',
                    '0x38c6A68304cdEfb9BEc48BbFaABA5C5B47818bb2',
                    ]:
                    t = DeFiContract(token, 'ERC20Fixed3')
                    name = t.NAME()
                    symbol = t.SYMBOL()
                else:
                    name = t.getName()
                    symbol = t.getSymbol()
                decimals = 18
                print('{} {}({}) {}'.format(token, name, symbol, decimals))
                db.save_token({
                    'address': token,
                    'name': name,
                    'symbol': symbol,
                    'decimals': decimals,
                })
            except exceptions.BadFunctionCallOutput:
                if token == '0xE0B7927c4aF23765Cb51314A0E0521A9645F0E2A':
                    name = 'DigixDAO'
                    symbol = 'DGD'
                decimals = 9
                print('{} {}({}) {}'.format(token, name, symbol, decimals))
                db.save_token({
                    'address': token,
                    'name': name,
                    'symbol': symbol,
                    'decimals': decimals,
                })