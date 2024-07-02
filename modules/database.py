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
            Denominations BIGINT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS PurchaserTransactions (
            DateOfPurchase DATE,
            DateOfExpiry DATE,
            PurchaserName TEXT,
            BondNumber INTEGER,
            Denominations BIGINT   
        )
    ''')
    return conn


def insert_data_into_db(conn, df, table_name):
    # just keep coloumns which are in db
    if table_name == 'PartyTransactions':
        df = df[['DateOfEncashment', 'PartyName', 'BondNumber', 'Denominations']]
    else:
        df = df[['DateOfPurchase', 'DateOfExpiry', 'PurchaserName', 'BondNumber', 'Denominations']]
    df.to_sql(table_name, conn, if_exists='append', index=False)
    
def connect(db_path=r'static\db\political_bonds.db'):
    return sqlite3.connect(db_path)