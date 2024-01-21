import psycopg2
from utility.logger import Logger

class PostgresHelper:

    def __init__(self, postgres_config, debug: bool = False):
        self.debug = debug
        self.postgres_config = postgres_config
        self.connection = None
        self.cursor = None

    def connect(self):
        if self.connection is None or self.connection.closed:
            self.connection = psycopg2.connect(**self.postgres_config)
            self.cursor = self.connection.cursor()

    '''
        For SELECT queries, fetch and return the results,
        For non-SELECT queries (INSERT, UPDATE, DELETE), commit and return None'''
    def run_sql(self, query, params=None):
        self.connect()
        try:
            self.cursor.execute(query, params) if params else self.cursor.execute(query)
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
        except psycopg2.Error as e:
            if self.debug:
                print(f"Database error: {e}")
            self.connection.rollback()
        finally:
            self.cursor.close()
            self.connection.close()

    def close(self):
        if self.connection and self.connection.closed == 0:
            self.connection.close()
                
    def find_one(self, table, where_clause, params):
        query = f"SELECT * FROM {table} WHERE {where_clause}"
        return self.run_sql(query, params, self.get_connection_params())
    
    def get_all(self, table, where_clause=None, params=None, limit=None):
        query = f"SELECT * FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"
        if limit:
            query += f" LIMIT {limit}"
        return self.run_sql(query, params, self.get_connection_params())
    
    def exists(self, table, where_clause, params):
        query = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {where_clause})"
        result = self.run_sql(query, params, self.get_connection_params())
        return result[0][0]
    
    def insert_transaction(self, transaction):
        insert_query = """
        INSERT INTO evm_chains.transactions (
            tx_id, block_number, timestamp, from_address, to_address, value,
            gas_price, gas_used, chain_id, input_data, transaction_fee
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (tx_id) DO NOTHING;
        """
        result = self.run_sql(insert_query, transaction)
        return result

    
    
