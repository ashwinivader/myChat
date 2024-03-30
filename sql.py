
import os
from dotenv import load_dotenv
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, types
from datamodels import mysql_data_types
load_dotenv()
sqlserver=os.getenv("sqlserver")
sqlusername=os.getenv("sqlusername")
sqlpassword=os.getenv("sqlpassword")

class sqlcreate:

    def __init__(self,dbname):
          load_dotenv()
          self.sqlserver=os.getenv("sqlserver")
          self.sqlusername=os.getenv("sqlusername")
          self.sqlpassword=os.getenv("sqlpassword")
          self.database=dbname
          # Create database 
          try:
             conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.sqlserver};UID={self.sqlusername};PWD={self.sqlpassword}')
             cursor = conn.cursor()
              # Execute the SQL query
             create_db_query = f"CREATE DATABASE [{dbname}]"
             cursor.execute(create_db_query)
             print("Database created successfully.")
          except pyodbc.Error as e:
            print(f"Error creating database: {e}")
            cursor.close   
            conn.close 


    def create_dataframe_from_excel(self,file_path):
     try:
        filename= os.path.splitext(os.path.basename(file_path))[0]
        print(file_path)
        # Read Excel file into a DataFrame
        filename = pd.read_excel(file_path)
        print(filename.head(5))
        return (filename)
     except Exception as e:
        print(f"Error occurred while reading Excel file: {e}")
        return None     



    def create_table(self,dataframe,tablenm):
          # Connect to SQL Server
          server = self.sqlserver
          username =self.sqlusername
          password = self.sqlpassword
          conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE=ashwini;UID={username};PWD={password}')
          cursor = conn.cursor()
          #print("=================dtypes=============")
          #print(dataframe.dtypes)


          # Define the MySQL table creation statement
          tablenm=tablenm.replace(" ", "")
          create_table_sql = f"CREATE TABLE {tablenm} ("
          # Iterate over DataFrame columns to create the table  that is to create query.
          columns=""
          for col_name, dtype in dataframe.dtypes.items():
             mysql_data_type = mysql_data_types[str(dtype)]
             col_name=col_name.replace(" ", "")
             create_table_sql += f"{col_name} {mysql_data_type}, "
          # Remove the trailing comma and space
          create_table_sql = create_table_sql[:-2]
          # Complete the CREATE TABLE statement
          create_table_sql += ");"
          #print(create_table_sql)


          try:
          # Delete the table if it exists
            drop_table_sql = f"DROP TABLE IF EXISTS {tablenm};"
            cursor.execute(drop_table_sql)   
            # Commit the transaction
            conn.commit()
          except Exception as e:
             print(f"Error occurred while dropping table: {e}")
          cursor.execute(create_table_sql)
          conn.commit()
          print("Table created successfully.")
          #print("===========columns==================")
          #print(columns)

          #add data into table using dataframe
          try:
            for index, row in dataframe.iterrows():
                row=tuple(row)
                insert_query = f"INSERT INTO {tablenm} VALUES {row}"
                #print(insert_query)
                cursor.execute(insert_query)
            conn.commit()      
            print("Data inserted successfully.")
            #return table name
            return(tablenm)
          except Exception as e:
            print(f"Error occurred while inserting data into table: {e}")
          finally:
              # Close the cursor and connection
            cursor.close()
            conn.close()



     


    

