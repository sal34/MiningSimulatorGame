import requests
import json

def getData():
    #print ("Loading realtime data..")
    #Get difficulty data and recent block
    """
    curl -X POST https://bitcoin-mainnet.public.blastapi.io -H 'Content-Type: application/json' -d '{"jsonrpc":"1.0","id":0,"method":"getblockchaininfo"}'
    """
    
    
    url = "https://bitcoin-mainnet.public.blastapi.io"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "1.0",
        "id": 0,
        "method": "getblockchaininfo"
    }
    
    try:
        response_json = requests.post(url, headers=headers, json=data).json()
    except requests.exceptions as e:
        print (f'Error on request <<getblockchaininfo: failed>>: {str(e)}')

        
    #Get diff and format it for Tera Diff.
    diff = response_json['result']['difficulty']
    fdiff = response_json['result']['difficulty']
    # Convert difficulty to terahashes (1 TH = 10^12 hashes)
    difficulty_terahashes = diff / 10**12
    # Format the difficulty value to display in terahashes with 2 decimal places
    diff = "{:.2f}T".format(difficulty_terahashes)
    
    
    block = response_json['result']['blocks']
    
    #print("Difficulty:", diff, "\nCurrent Block: ", block)

    #Get block hash
    
    """
    curl -X POST https://bitcoin-mainnet.public.blastapi.io -H 'Content-Type: application/json' -d '{"jsonrpc":"1.0","id":0,"method":"getblockhash","params":[800]}'
    """
    oldblock = block-1
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "1.0",
        "id": 0,
        "method": "getblockhash",
        "params": [oldblock]
    }
    
    try:
        response_json = requests.post(url, headers=headers, json=data).json()
    except requests.exceptions as e2:
        print (f'Error on request <<getblockhash: failed>>: {str(e2)}')

    hash = response_json['result']

    #Get last BTC to USD conversion price
    try:
        conversion = requests.post("https://cex.io/api/last_price/BTC/USD").json()
        conversion = conversion['lprice']
    except requests.exceptions as e3:
        conversion = 0
        print (f'Error on request <<lprice: failed>>: {str(e3)}')

    #print(f'Hash of the block {block-1}: {hash}')
    #print ("Realtime data loaded, and up to date. \n\n")
    
    #Information variables: oldblock (current block -1), block (current block), diff (current new block difficulty on the net), hash (oldblock hash, the new need to be calculated from the net).
    
    #Current data show
    #print("Difficulty: ", diff,
         # "\nCurrent Block: ", block,
         # "\nOld Block: ", oldblock,
         # "\nOld Block Hash: ", hash)
    
    return diff, block, oldblock, hash, fdiff, conversion


def btcusd():
    try:
        conversion = requests.post("https://cex.io/api/last_price/BTC/USD").json()
        conversion = conversion['lprice']
    except requests.exceptions as e3:
        conversion = 0
        print (f'Error on request <<lprice: failed>>: {str(e3)}')
    return conversion
