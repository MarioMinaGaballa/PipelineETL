import sys
from urllib.parse import quote_plus
import pandas as pd
import sqlalchemy
#source csv file path
csv_path = r'C:\Users\Mario\OneDrive\Desktop\PyETL\DataSources\customers.csv'
#target database connection string
target_odbc = (
    r'Driver={ODBC Driver 17 for SQL Server};'
    r'Server=LAPTOP-SVBHR95T\SQLEXPRESS;'
    r'Database=StagingLayer;'
    r'Trusted_Connection=yes;'
)

target_engine = sqlalchemy.create_engine(
    f"mssql+pyodbc:///?odbc_connect={quote_plus(target_odbc)}",
    fast_executemany=True,
)

# Extract
dataframe = pd.read_csv(csv_path, dtype={'phone': str, 'zip_code': str})
print(dataframe.head(10))

# Load
try:
    dataframe.to_sql('test_Customers', con=target_engine, if_exists='replace', index=False)
    print(f"{len(dataframe)} rows loaded")
except Exception as e:
    print("Error exporting to database:", e)
    sys.exit(1)