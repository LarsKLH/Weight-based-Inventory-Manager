-- db_setup.sql

-- Create Storage table
CREATE TABLE IF NOT EXISTS Storage (
    storage_id VARCHAR PRIMARY KEY,
    tot_weight FLOAT,
    weight_pr FLOAT
);

-- Create Calendar table
CREATE TABLE IF NOT EXISTS Calendar (
    datetime_id VARCHAR PRIMARY KEY,
    operation_id VARCHAR
);

-- Create Operations table
CREATE TABLE IF NOT EXISTS Operations (
    operation_id VARCHAR PRIMARY KEY,
    procedure_link VARCHAR
);

-- Create Operation_Storage_map table
CREATE TABLE IF NOT EXISTS Operation_Storage_map (
    map_id INTEGER PRIMARY KEY,
    operation_id VARCHAR,
    storage_id VARCHAR,
    quantity INTEGER,
    FOREIGN KEY (operation_id) REFERENCES Operations(operation_id),
    FOREIGN KEY (storage_id) REFERENCES Storage(storage_id)
);

-- Create Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    storage_id VARCHAR,
    quantity INTEGER,
    order_date VARCHAR,
    received_date VARCHAR,
    FOREIGN KEY (storage_id) REFERENCES Storage(storage_id)
);