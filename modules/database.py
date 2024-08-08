# modules/database.py
import sqlite3

# def create_database():
#     conn = sqlite3.connect(r'static\db\political_bonds.db')
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS PartyTransactions (
#             SrNo INTEGER,
#             DateOfEncashment DATE,
#             PartyName TEXT,
#             PartyAccountNo TEXT,
#             Prefix TEXT,
#             BondNumber INTEGER,
#             Denominations BIGINT,
#             PayBranchCode TEXT,
#             PayTeller TEXT
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS PurchaserTransactions (
#             SrNo INTEGER,
#             ReferenceNo TEXT,
#             JournalDate DATE,
#             DateOfPurchase DATE,
#             DateOfExpiry DATE,
#             PurchaserName TEXT,
#             Prefix TEXT,
#             BondNumber INTEGER,
#             Denominations BIGINT,
#             IssueBranchCode TEXT,
#             IssueTeller TEXT,
#             Status TEXT    
#         )
#     ''')
#     return conn

def create_database():
    conn = sqlite3.connect(r'static\db\political_bonds.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS PartyTransactions (
            DateOfEncashment DATE,
            PartyName TEXT,
            BondNumber INTEGER,
            Prefix TEXT,
            Denominations BIGINT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS PurchaserTransactions (
            DateOfPurchase DATE,
            DateOfExpiry DATE,
            PurchaserName TEXT,
            BondNumber INTEGER,
            Prefix TEXT,
            Denominations BIGINT   
        )
    ''')
    return conn


def insert_data_into_db(conn, df, table_name):
    if table_name == 'PartyTransactions':
        df = df[['DateOfEncashment', 'PartyName', 'BondNumber', 'Prefix' ,'Denominations']]
    else:
        df = df[['DateOfPurchase', 'DateOfExpiry', 'PurchaserName', 'BondNumber','Prefix' , 'Denominations']]
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
def connect(db_path=r'static\db\political_bonds.db'):
    return sqlite3.connect(db_path)


def get_table_preview(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
    return cursor.fetchall()

def get_table_columns(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    return [col[1] for col in columns]

def get_table_description(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    description = f"Table '{table_name}' has the following columns: " + ", ".join([col[1] + " (" + col[2] + ")" for col in columns])
    return description

def get_description_of_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    descriptions = {}
    for table in tables:
        table_name = table[0]
        descriptions[table_name] = get_table_description(conn, table_name)
        
    description_str = "\n\n".join([f"Table '{table}':\n{desc}" for table, desc in descriptions.items()])
    return description_str

def get_tables_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]