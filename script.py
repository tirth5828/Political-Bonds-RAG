import modules.extract as extract
import modules.database as db
import modules.query_processor as qp

def load_data():
    pdf1_path = r'static\pdf\Bond_Encashment.pdf'
    pdf2_path = r'static\pdf\Bond_Purchase.pdf'
    print('Starting data extraction process...')
    
    print(f'Extracting data from:\n1. {pdf1_path}\n2. {pdf2_path}')
    
    tables_pdf1 = extract.extract_data_from_pdf(pdf1_path)
    tables_pdf2 = extract.extract_data_from_pdf(pdf2_path)
    
    print(f'Extracted {len(tables_pdf1)} tables from {pdf1_path}')
    print(f'Extracted {len(tables_pdf2)} tables from {pdf2_path}')
    
    print('Creating database and inserting data...')
    conn = db.create_database()
    party_columns = ['SrNo', 'DateOfEncashment', 'PartyName', 'PartyAccountNo', 'Prefix' , 'BondNumber', 'Denominations', 'PayBranchCode', 'PayTeller']
    purchaser_columns = ['SrNo', 'ReferenceNo', 'JournalDate', 'DateOfPurchase', 'DateOfExpiry', 'PurchaserName', 'Prefix','BondNumber', 'Denominations', 'IssueBranchCode', 'IssueTeller', 'Status']
    
    for df1 in tables_pdf1:
        extract.clean_data(df1, party_columns, ['DateOfEncashment'])
        db.insert_data_into_db(conn, df1, 'PartyTransactions')

    for df2 in tables_pdf2:
        extract.clean_data(df2, purchaser_columns, ['JournalDate', 'DateOfPurchase', 'DateOfExpiry'])
        db.insert_data_into_db(conn, df2, 'PurchaserTransactions')
    
    conn.commit()
    conn.close()
    print("Database operations completed successfully.")

def process_queries_from_file(input_file, output_file , api_key):
    conn = db.connect()
    agent_executor = qp.create_agent(r'static\db\political_bonds.db' , api_key)

    with open(input_file, 'r') as f:
        questions = f.readlines()

    with open(output_file, 'w') as f:
        for question in questions:
            question = question.strip()
            if question:
                print(f"Processing query: {question}")
                answer, sql_query = qp.translate_and_execute_query(agent_executor, question)
                rows = qp.execute_sql_query(conn, sql_query)
                response = qp.format_response(rows)
                
                f.write(f"Question: {question}\n")
                f.write(f"Answer: {answer}\n")
                f.write(f"SQL Query: {sql_query}\n")
                f.write(f"Response: {response}\n\n")
                print(f"Processed query: {question}")

    conn.close()

if __name__ == '__main__':
    load_data()
    api_key = input("Enter your OpenAI API key: ")
    if not api_key:
        raise ValueError("API key is required to run the script.")
    process_queries_from_file('questions.txt', 'answers.txt' , api_key)
