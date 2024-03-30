#from pandasai import SmartDataframe
#from pandasai.connectors import MySQLConnector
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
import os
from dotenv import load_dotenv
import requests
from utils import getCollectionData

class mychat:
          
      def __init__(self,username):
          load_dotenv()
          self.server=os.getenv("sqlserver")
          self.username=os.getenv("sqlusername")
          self.password=os.getenv("sqlpassword")
          api_url = f"http://localhost:8000/getcollectiondata/{username}"
          #api_url="http://localhost:8000/items/123"
          response = requests.get(api_url)
          #response=getCollectionData(username)
          if response.status_code == 200:
             # Print the JSON response
            print(response.json())
          else:
            # Print an error message if the request was not successful
             print(f"Error: {response.status_code} - {response.reason}")

          #self.database=dbname
          #conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={dbname};UID={self.username};PWD={self.password}')
          #cursor = conn.cursor()   
"""
def main():
          load_dotenv()
          sqlserver=os.getenv("sqlserver")
          sqlusername=os.getenv("sqlusername")
          sqlpassword=os.getenv("sqlpassword")
          conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={sqlserver};DATABASE=ashwini;UID={sqlusername};PWD={sqlpassword}')
          cursor = conn.cursor()
          #cursor.execute("select * from FinancialSample")

          try:
             # Execute the query
                #query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'ashwini' AND table_name = 'FinancialSample'"
                #query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'ashwini' AND table_name = 'FinancialSample'"
                query="select * from FinancialSample"
                query="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'FinancialSample';"
                cursor.execute(query)

              # Fetch the results
                results = cursor.fetchall()
              # Process the results
                
                for row in results:
                    print(row)  # You can do further processing here
            #



              # Commit the transaction (optional for SELECT queries)
                #conn.commit()

          except Exception as e:
                print("Error:", e)

          finally:
               # Close the cursor and connection
                 cursor.close()
                 conn.close()

if __name__ == "__main__":
    main()
    """