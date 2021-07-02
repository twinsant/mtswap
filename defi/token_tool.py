from database import MongoDB
from helper import DeFiContract
from web3 import exceptions

def normalize_text(str):
    return w3.toText(str) if str.find("0x") > -1 else str

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
                t = DeFiContract(token, 'ERC20Fixed2')
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