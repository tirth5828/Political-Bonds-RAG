# modules/extract.py
import tabula
import pandas as pd

def extract_data_from_pdf(pdf_path, pages='all'):
    return tabula.read_pdf(pdf_path, pages=pages, multiple_tables=True)

def clean_data(df, column_names, date_columns):
    df.columns = column_names
    for date_col in date_columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
    df.loc[:, 'Denominations'] = df['Denominations'].str.replace(',', '').astype(int)
    return df
