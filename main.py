import streamlit as st
import modules.extract as extract
import modules.database as db
import modules.query_processor as qp
from tqdm import tqdm

def load_data():

    pdf1_path = r'static\pdf\Bond_Encashment.pdf'
    pdf2_path = r'static\pdf\Bond_Purchase.pdf'
    st.write('Starting data extraction process...')
    
    # Display PDF paths being processed
    st.write(f'Extracting data from:\n1. {pdf1_path}\n2. {pdf2_path}')
    
    # Start a progress bar
    progress_bar = st.progress(0)
    st.write('Loading PDF data...')
    tables_pdf1 = extract.extract_data_from_pdf(pdf1_path)
    # Update progress bar after loading first PDF
    progress_bar.progress(25)
    
    tables_pdf2 = extract.extract_data_from_pdf(pdf2_path)
    # Update progress bar after loading second PDF
    progress_bar.progress(50)
    st.write(f'Extracted {len(tables_pdf1)} tables from {pdf1_path}')
    st.write(f'Extracted {len(tables_pdf2)} tables from {pdf2_path}')
    
    st.write('Creating database and inserting data...')
    conn = db.create_database()
    party_columns = ['SrNo', 'DateOfEncashment', 'PartyName', 'PartyAccountNo', 'Prefix' , 'BondNumber', 'Denominations', 'PayBranchCode', 'PayTeller']
    purchaser_columns = ['SrNo', 'ReferenceNo', 'JournalDate', 'DateOfPurchase', 'DateOfExpiry', 'PurchaserName', 'Prefix','BondNumber', 'Denominations', 'IssueBranchCode', 'IssueTeller', 'Status']
    
        
    
    # Insert data into the database with updates to the progress bar
    for index, df1 in enumerate(tables_pdf1, start=1):
        extract.clean_data(df1, party_columns, ['DateOfEncashment'])
        db.insert_data_into_db(conn, df1, 'PartyTransactions')
        progress_bar.progress(50 + (25 * index) // len(tables_pdf1))

    for index, df2 in enumerate(tables_pdf2, start=1):
        extract.clean_data(df2, purchaser_columns, ['JournalDate', 'DateOfPurchase', 'DateOfExpiry'])
        db.insert_data_into_db(conn, df2, 'PurchaserTransactions')
        progress_bar.progress(75 + (25 * index) // len(tables_pdf2))
    
    # Finalize the database operations
    conn.commit()
    conn.close()
    progress_bar.progress(100)  # Complete the progress bar
    st.write("Database operations completed successfully.")
    st.balloons()  # Celebrate the completion

def main():
    st.title('Political Bonds Data Processing')
    st.balloons()
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    if st.button('Load Data'):
        load_data()

    conn = db.connect()
    
    user_query = st.text_input("Please enter your query in natural language:")
    
    if st.button('Execute Query'):
        if user_query:
            with st.spinner('Processing your query...'):
                agent_executor = qp.create_agent(r'static\db\political_bonds.db' , api_key)
                answer , sql_query = qp.translate_and_execute_query(agent_executor, user_query)
                rows = qp.execute_sql_query(conn, sql_query)
                response = qp.format_response(rows)
                st.write(f"Answer as sentence : {answer}")
                st.caption(f"Sql Query : {sql_query}")
                st.success(response)
        else:
            st.write("Please enter a query to execute.")
    
    conn.close()

if __name__ == '__main__':
    main()