import concurrent.futures
import sys
import traceback

from database import MongoDB
from helper import DeFiContract
from web3 import exceptions

def parse_token(token):
    try:
        t = DeFiContract(token, 'ERC20')
        name = t.name()
        symbol = t.symbol()
        decimals = t.decimals()
    except OverflowError:
        # https://www.gitmemory.com/issue/blockchain-etl/ethereum-etl/240/796883933
        t = DeFiContract(token, 'ERC20Fixed')
        name = t.name().decode('utf-8')
        symbol = t.symbol().decode('utf-8')
        decimals = t.decimals()
    except exceptions.ContractLogicError:
        name = 'ContractLogicError'
        symbol = 'ERR'
        decimals = 18
    except exceptions.BadFunctionCallOutput:
        name = 'BadFunctionCallOutput'
        symbol = 'ERR'
        decimals = 18
    except Exception as e:
        traceback.print_exc()
        sys.exit(-1)
    print('{} {}({}) {}'.format(token, name, symbol, decimals))
    doc = {
        'address': token,
        'name': name,
        'symbol': symbol,
        'decimals': decimals,
    }
    return doc

if __name__ == '__main__':
    db = MongoDB()
    tokens = db.get_all_tokens()
    parse_tokens = []
    for token in tokens:
        if db.get_token(token) is None:
            parse_tokens.append(token)
            # if len(parse_tokens) == 6:
            #     break
    print(len(parse_tokens))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for token in parse_tokens:
            futures.append(executor.submit(parse_token, token))
        for future in concurrent.futures.as_completed(futures):
            doc = future.result()
            print(doc)
            if doc:
                db.save_token(doc)