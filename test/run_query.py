import modules.database as db
from tqdm import tqdm
import modules.query_processor as qp


sql_query = "SELECT SUM(Denominations) FROM PurchaserTransactions WHERE PurchaserName = 'CHOUDHARY GARMENTS' AND DateOfPurchase = '2019-04-12'"

conn = db.connect(r"static\db\political_bonds.db")
if sql_query:
    print(f"Translated SQL Query: {sql_query}")
    rows = qp.execute_sql_query(conn, sql_query)
    print(rows)
    # formatted_response = qp.format_response(rows)
    # print("Query Results:")
    # print(formatted_response)
else:
    print("No valid SQL query could be generated.")