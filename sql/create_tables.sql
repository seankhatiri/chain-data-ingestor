CREATE TABLE evm_chains.transactions (
    tx_id VARCHAR PRIMARY KEY,
    block_number INTEGER, -- REFERENCES blocks(block_number),
    timestamp TIMESTAMP,
    from_address VARCHAR, -- REFERENCES addresses(address),
    to_address VARCHAR, -- REFERENCES addresses(address),
    value NUMERIC,
    gas_price NUMERIC,
    gas_used NUMERIC,
    chain_id INTEGER,
    input_data TEXT,
    transaction_fee NUMERIC
);

-- -- TODO: Add block and address tables
-- CREATE TABLE blocks (
--     block_number INTEGER PRIMARY KEY,
--     miner VARCHAR,
-- );

-- CREATE TABLE addresses (
--     address VARCHAR PRIMARY KEY,
-- );