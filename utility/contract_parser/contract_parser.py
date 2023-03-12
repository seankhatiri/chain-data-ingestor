import pandas as pd
import json
import subprocess
import sys
import glob
import sys
import os
from pathlib import Path
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from connector.mongo_helper import MongoHelper
from configuration.configs import Configs


class ContractParser:

    def __init__(self):
        self.mongo_helper = MongoHelper(Configs.mongo_url)

    #first create json file for all contracts we have
    def _create_contracts_json(self):
        results = self.mongo_helper.get_all('contracts')
        for result in results:
            body = self._get_body(result['SourceCode'], result['ABI'], result['ContractName'], result['Proxy'])
            with open(f"data/{result['contractAddress']}.json", "w") as f:
                json.dump(body, f)
    
    def _get_body(self, source_code, abi, contract_name, proxy):
        return {
            "SourceCode": f"{source_code}",
            "ABI": f"{abi}",
            "ContractName": f"{contract_name}",
            "CompilerVersion": "",
            "OptimizationUsed": "",
            "Runs": "",
            "ConstructorArguments": "", 
            "EVMVersion": "", 
            "Library": "",
            "LicenseType": "", 
            "Proxy": f"{proxy}", 
            "Implementation": "", 
            "SwarmSource": ""
        }

    def _create_parsed_contracts(self):
        self._create_contracts_json()
        #contract2paraquet
        cmd1 = "python"
        args1 = ["script/2parquet.py", "-s", "data", "-o", "data/parquet", "--threshold", "0.9"]
        process1 = subprocess.Popen([cmd1] + args1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #flatened
        cmd2 = "python"
        args2 = ["script/filter_data.py", "-s", "data/parquet", "-o", "data/flattened", "--threshold", "0.9"]
        process2 = subprocess.Popen([cmd2] + args2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #Inflated
        cmd3 = "python"
        args3 = ["script/filter_data.py", "-s", "parquet", "-o", "data/inflated", "--split-files", "--threshold", "0.9"]
        process3 = subprocess.Popen([cmd3] + args3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #parse contract
        cmd4 = "python"
        args4 = ["script/parse_data.py", "-s", "data/inflated", "-o", "data/parsed"]
        process3 = subprocess.Popen([cmd4] + args4, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def update_contract(self, df, contract_address):
        # for each contract_address in paraq, get classes -> contracts_code, for each class get funcs and for each func get comment 
        # and code, update the contract's classes and class['funcs]
    
        # Filter the DataFrame to only include rows for the given contract address
        contract_df = df[df['contract_address'] == contract_address]
        # Initialize an empty list to hold the contract's classes
        classes = []
        # Group the DataFrame by class name
        grouped = contract_df.groupby('class_name')
        # Iterate over each group (i.e. each class) and extract its information
        for class_name, class_df in grouped:
            # Extract the class code and documentation from the first row in the group
            class_code = class_df.iloc[0]['class_code']
            class_documentation = class_df.iloc[0]['class_documentation']
            # Initialize an empty list to hold the class's functions
            funcs = []
            # Iterate over each row in the group and extract the function information
            for _, row in class_df.iterrows():
                func_name = row['func_name']
                func_code = row['func_code']
                func_documentation = row['func_documentation']
                # Add the function information to the list of functions
                funcs.append({
                    'func_name': func_name,
                    'func_code': func_code,
                    'func_documentation': func_documentation
                })
            # Add the class information (including its list of functions) to the list of classes
            classes.append({
                'class_name': class_name,
                'class_code': class_code,
                'class_documentation': class_documentation,
                'funcs': funcs
            })
        # Return a dictionary containing the list of classes for the given contract address
        return {'classes': classes}

    def run(self):
        file_paths = glob.glob('utility/contract_parser/data/parsed/*.parquet')
        df = pd.concat([pd.read_parquet(fp) for fp in file_paths])
        print('The datafram has been loaded')
        contracts = self.mongo_helper.get_all('contracts', limit=1)
        for contract in contracts:
            self.mongo_helper.update_one({'contractAddress': contract['contractAddress']}, self.update_contract(df, contract['contractAddress']), 'contracts')
            print(f"contract {contract['contractAddress']} has been updated")

if __name__ == '__main__':
    ContractParser().run()