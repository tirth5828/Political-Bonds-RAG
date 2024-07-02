
# Political Bonds Data Processing Project

## Overview
This project extracts data from PDF files containing details about political bonds, stores this data in a SQLite database, and provides a Streamlit web interface to interact with the data. Users can query the database using natural language through the web interface, which leverages an AI model to convert these queries into SQL statements.

## Features
- **PDF Data Extraction**: Extracts tables from PDF documents and parses them into structured data.
- **Database Storage**: Loads extracted data into a SQLite database for easy querying.
- **Natural Language Queries**: Allows users to enter queries in natural language and converts these into SQL queries.
- **Streamlit Web Interface**: Provides a user-friendly interface to interact with the data.

## Project Structure
```
political_bonds/
│
├── modules/
│   ├── __init__.py
│   ├── database.py          # Module to handle database operations
│   ├── extract.py           # Module to extract data from PDFs
│   └── query_processor.py   # Module to process queries using AI
│
├── static/
│   ├── pdf/                 # Directory containing PDF files
│   └── db/                  # Directory containing SQLite database file
│
└── main.py                  # Main script to run the Streamlit app
```

## Setup
### Requirements
- Python 3.8+
- Streamlit
- SQLite3
- Additional Python libraries: `pandas`, `sqlalchemy`, `tqdm`, `transformers[torch]`

### Installation
1. Clone the repository:
   ```
   git clone https://your-repository-url
   cd political_bonds
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Data Setup
Ensure that the PDF files are placed under `static/pdf/` directory.

## Running the Application
To run the Streamlit application:
```
streamlit run main.py
```
This will start the server and open the web interface in your default web browser.

## Usage
- **Loading Data**: Click the 'Load Data' button on the web interface to extract data from the PDFs and load it into the database.
- **Querying Data**: Enter your natural language query in the text input box and press 'Execute Query' to see the results.

