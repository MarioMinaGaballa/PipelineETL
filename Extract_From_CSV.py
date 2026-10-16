import sys
import pandas as pd
import pyodbc

connection_string = (
    r'Driver={ODBC Driver 17 for SQL Server};'
    r'server=LAPTOP-SVBHR95T\SQLEXPRESS;'
    r'database=testingDB;'
    r'trusted_connection=yes;'
)

csv_path = r'C:\Users\Mario\OneDrive\Desktop\PyETL\DataSources\customers.csv'

cols = ['customer_id', 'first_name', 'last_name', 'phone', 'email',
        'street', 'city', 'state', 'zip_code']

# Extract
dataframe = pd.read_csv(csv_path, dtype={'phone': str, 'zip_code': str})
print(dataframe.head(10))

# Connect
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print("Error connecting to database:", e)
    sys.exit(1)

cursor = conn.cursor()

# Transform (تحويل NaN إلى None)
data = dataframe[cols].astype(object).where(dataframe[cols].notnull(), None).values.tolist()

# Load
try:
    cursor.execute("TRUNCATE TABLE StagingLayer.dbo.Customers")  # عشان إعادة التشغيل متكررش الداتا
    cursor.fast_executemany = True
    cursor.executemany(
        """INSERT INTO StagingLayer.dbo.Customers
           (CustomerID, first_name, last_name, phone, email, street, city, state, zip_code)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        data
    )
    conn.commit()
    print(f"{len(data)} rows inserted successfully!")
except Exception as e:
    conn.rollback()
    print("Error inserting data:", e)
finally:
    conn.close()