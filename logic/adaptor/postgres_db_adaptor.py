from configuration.configs import Configs
from connector.postgres_helper import PostgresHelper
from logic.adaptor.adaptor import Adaptor

class PostgresDBAdaptor(Adaptor):

    def __init__(self):
        self.postgres_helper = PostgresHelper(Configs.postgres_config)

    def fetch_transactions(self):
        raise NotImplementedError()
    