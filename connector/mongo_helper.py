from pprint import pprint

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

from utility.logger import Logger


class MongoHelper:
    debug: bool
    url: str
    client: MongoClient
    db: Database

    def __init__(self, url, debug: bool = False):
        self.debug = debug
        self.url = url
        self.connect()

    def connect(self):
        self.client = MongoClient(self.url, server_api=ServerApi('1'))
        dbs = self.client.list_database_names()
        self.db = self.client.get_default_database(default='test')
        # server_status_result = self.db.command("serverStatus")
        # pprint(server_status_result)

    def drop_collection(self, collection_name):
        try:
            self.db[collection_name].drop()
        except Exception as e:
            Logger().error(str(e), title='drop collection', additional_data=collection_name)

    def insert_all(self, data, collection_name):
        if data is None or len(data) == 0:
            return False, None
        try:
            ids = self.db[collection_name].insert_many(data, ordered=False)
            return True, ids
        except Exception as e:
            Logger().error(e, title='insert to db', additional_data={
                'collection name': collection_name
            })
            return False, None

    def insert_one(self, data, collection_name):
        try:
            ids = self.db[collection_name].insert_one(data)
            return True, ids
        except Exception as e:
            print(str(e))
            return False, None

    def bulk_update(self, data, collection_name):
        bulk = self.db[collection_name].initialize_ordered_bulk_op()
        # for document in data:
        #     if 'Photos' in document:
        #         bulk.find({'_id': document['_id']}).update({'$set': {'Photos': document['Photos'], }})
        # bulk.execute()

    def update_many(self, condition, data, collection_name, upsert=False):
        return self.db[collection_name].update_many(condition, data, upsert=upsert)

    def update_one(self, condition, data, collection_name, upsert=False):
        return self.db[collection_name].update(condition, data, upsert=upsert)

    def get_all(self, collection_name, condition=None, limit=None):
        if limit is None:
            result = self.db[collection_name].find(condition).batch_size(100)
        else:
            result = self.db[collection_name].find(condition).limit(limit).batch_size(100)

        results = []
        for data in result:
            results.append(data)
        return results

    def find_one(self, collection_name, filter):
        result = self.db[collection_name].find_one(filter)
        return result

    def get_count(self, collection_name, condition=None, aggregation=None):
        result = None
        if aggregation:
            result = \
                len(list(self.db[collection_name].aggregate(aggregation)))
        elif condition:
            result = self.db[collection_name].count_documents(condition)
        return result

    def delete_many(self, collection_name, condition=None):
        self.db[collection_name].delete_many(condition)

    def exists(self, collection_name, condition):
        return self.db[collection_name].count_documents(condition) > 0

    def aggregate(self, collection_name, aggr_pipeline):
        return list(self.db[collection_name].aggregate(aggr_pipeline))

    def is_contract(self, address):
        return self.exists('contracts', {'contractAddress': address})
    
    def cache_contract(self, address, data):
        contract = {
            'contractAddress': address,
            'SourceCode': data['SourceCode'],
            'ABI': data['ABI'],
            'ContractName': data['ContractName'],
            'Proxy': data['Proxy']
        }
        self.insert_one(contract, 'contracts')
    



