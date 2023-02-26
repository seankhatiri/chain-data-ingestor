from typing import Any
from eth_abi import decode_abi
from web3 import Web3

class Decoder:
    function_signature: Any
    encoded_params: Any

    def __init__(self):
        pass

    def run(self, abi_encoding):
        self.function_signature = abi_encoding[:10]
        self.encoded_params = abi_encoding[10:]
        return self._function_name()


    def _function_name(self):
        # Instantiate a web3 provider (e.g. Infura)
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/8f890b3a78e740f2bd98be613da634f1'))

        # Use the web3 function signature to get the corresponding function name
        function_name = w3.eth.abi.decode_function_selector(self.function_signature)

        return function_name # Output: transfer(address,uint256)