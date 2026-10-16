## for accessing and reading from Sql
import pandas as pd
import os 

import pyodbc
import sqlalchemy


drivers = pyodbc.drivers()
# print(drivers)

connection_string =(
  r'Driver={ODBC Driver 17 for SQL Server};'
  r'server=LAPTOP-SVBHR95T\SQLEXPRESS;'
  r'database=testingDB;'
  r'trusted_connection=yes;'
)

try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
except Exception as e:
    print("Error connecting to database:", e) 
  
cursor = conn.cursor()

# to Run sql queries, we need to create a cursor object. The cursor is used to execute SQL commands and retrieve data from the database.
# cursor = conn.cursor()   
# cursor.execute("select * into StagingLayer from testingDB.dbo.Employees")
# for row in cursor.fetchall():
#   print(row)
#   conn.close()

# query ="select * from testingDB.dbo.Employees"
# employees_df = pd.read_sql(query, conn)
# print(employees_df.head())
# conn.close()


## move tabel on testingDB to StagingLayer (Another database) using SQL query
# cursor.execute("SELECT * INTO StagingLayer.dbo.Employees FROM testingDB.dbo.Employees")
# conn.commit()
cursor.execute("SELECT * FROM StagingLayer.dbo.Employees")
for row in cursor.fetchall():
  print(row)
  conn.close()