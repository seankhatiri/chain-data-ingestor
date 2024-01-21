# TODO: recieve the SQL query, run againest db, return the results

from connector.postgres_helper import PostgresHelper
from utility.singleton import Singleton
from configuration.configs import Configs

class QueryEngineController(metaclass=Singleton):

    def __init__(self):
        self.postgres_helper = PostgresHelper(Configs.postgres_config)

    def run(self, query):
        results = self.postgres_helper.run_sql(query)
        return results
