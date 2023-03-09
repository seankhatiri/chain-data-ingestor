#TODO: if it's token add description, I have the src and dest, just need the func_name and args which I think Patrck got them
from web3 import Web3
import json

import requests
from bs4 import BeautifulSoup

# Connect to an Ethereum node using Web3
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/8f890b3a78e740f2bd98be613da634f1'))

# Define the transaction hash to fetch and decode
tx_hash = '0xe5fb8b777525bf675759eb188c1f8d812784b96843ae6356ed3414652cefe585'

tx = w3.eth.getTransaction(tx_hash)
src_address = tx['from']
dest_address = tx['to']
input_data = tx['input']
print(f"Source address: {src_address}")
print(f"Destination address: {dest_address}")
print(f"Input data: {input_data}")

# tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
# contract_address = tx_receipt['contractAddress']
# print(contract_address)
# # contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
# etherscan_api_key = 'D2QM9JPD6UMK1XYCTK32SE9IRZCP8BF1AG'
# abi_request = f'https://api.etherscan.io/api?module=contract&action=getabi&address={dest_address}&apikey={etherscan_api_key}'
# response = requests.get(abi_request)
# abi_json = response.json()
# abi = abi_json['result']

# function_signature = input_data[:10]
# function_abi = next(item for item in abi if item["type"] == "function" and encode_abi_packed(['bytes4'], [item['signature']]) == function_signature)
# decoded_input = decode_abi([arg["type"] for arg in function_abi["inputs"]], input_data[10:])
# print(f"Decoded input: {decoded_input}")

