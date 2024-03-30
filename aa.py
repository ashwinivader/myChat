import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine
import pymysql
import csv
import openpyxl


def mysql_connection():
   dbuser="root"
   dbpassword="root"
   dbhost="127.0.0.1"
   dbport="3306"
   dbname="analysis"
   sql_conn_str=f"mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}/{dbname}"
   conn=create_engine(sql_conn_str)
   return(conn)


def read_structred_csv_file(filepath):
    dfs={}   
    try:
        df = pd.read_csv(filepath,)
        file_name_with_extension = os.path.basename(filepath)  # Get the base name of the file with extension
        file_name_without_extension = os.path.splitext(file_name_with_extension)[0]  # Extract the file name without extension
        rowstoskip=get_rows_to_skip_csv(filepath)
        #print(rowstoskip)
        df = pd.read_csv(filepath,skiprows=rowstoskip)
        sheetname=file_name_without_extension
        dfs[sheetname]=df    
        return(dfs)       
    except Exception as e:
        print('Error reading csv file: %s' % e)
        raise Exception('Error reading csv file: %s' % e)  


def read_structred_excel_file(filepath):
    dfs={}
    try:

        sheet_names=pd.ExcelFile(filepath).sheet_names 
        #loop through all sheets and create xls.Created dictionary to store dataframes for each sheet
        for sheet in sheet_names:
            rowtoskip=get_rows_to_skip_xls(filepath,sheet)
            #print("========rowtoskip=======",f'{rowtoskip}',sheet)  
            df = pd.read_excel(filepath, sheet_name=sheet,skiprows=rowtoskip)
            dfs[sheet]=df
        return(dfs)       
    except Exception as e:
        print('Error reading xls file: %s' % e)
        raise Exception('Error reading xls file: %s' % e)
    

def save_to_sql(dfs:dict,id):
    #print(id)
    #print(type(id))   
    conn= mysql_connection()
    table_info = {}
    #(key+""+id) is table name while values in dfs[key] is dataframe which is table data
    for key in dfs.keys():
       dfdata = dfs[key] 
       fields=dfs[key].columns
       tbname=str.lower(key+"_"+id)
       dfdata.to_sql(tbname,conn,index=False,if_exists='replace') 
       table_info[tbname] = fields 
       #print(tbname) 
       #print(fields)    
    conn.dispose()
    result = {
        "tables": table_info
    }
    result=get_table_schema(id)
    #print(result)
    return(result)

def execute_sql_query(query,doc_id,limit=10000): 
        pattern="%"+doc_id+"%"
        engine= mysql_connection()
        result = pd.read_sql_query(query, engine, params=(pattern,))
        result = result.infer_objects()
        #print(result)
        for col in result.columns:  
            if 'date' in col.lower(): result[col] = pd.to_datetime(result[col], errors="ignore")  
        if limit is not None: result = result.head(limit)
        return result


def get_table_schema(doc_id):    
    sql_query = """SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name LIKE %s"""
    df = execute_sql_query(sql_query,doc_id, limit=None)  
    output=[] 
    current_table = ''  
    columns = []  
    for index, row in df.iterrows():
        table_name = f"{row['TABLE_NAME']}" 
        column_name = row['COLUMN_NAME']  
        data_type = row['DATA_TYPE']   
        table_name=  f"[{table_name}]"
        #if " " in table_name: table_name= f"[{table_name}]" 
        column_name = row['COLUMN_NAME']  
        column_name= f"[{column_name}]"
        #if " " in column_name: column_name= f"[{column_name}]" 
        if current_table != table_name and current_table != '':  
            output.append(f"table: {current_table}, columns: {', '.join(columns)}")  
            columns = []  
        columns.append(f"{column_name} {data_type}")  
        current_table = table_name  

    output.append(f"table: {current_table}, columns: {', '.join(columns)}")
    output = "\n ".join(output)
    #print(output)
    return output


def get_rows_to_skip_xls(filepath, sheet_name):
    workbook = openpyxl.load_workbook(filepath)
    # Select the specified sheet
    sheet = workbook[sheet_name]
    nonnulllist = []
    i = 0  # Initialize a counter for the number of rows iterated
    for row in sheet.iter_rows():
        if i >= 10:  # Limit the iteration to the first 15 rows
            break
        non_null_count = sum(1 for cell in row if cell.value is not None)  # Count non-null cells in the row
        nonnulllist.append(non_null_count)
        i += 1  
    max_index = nonnulllist.index(max(nonnulllist))
    return max_index


def get_rows_to_skip_csv(filepath):
     # Initialize an empty list to store the counts of non-null cells in each row
    non_null_counts = []
    with open(filepath, 'r') as file:
      reader = csv.reader(file)  
      i=0  
      for row in reader:
          if i>=10:
              break;
          # Count the number of non-null cells in the row
          non_null_count = sum(1 for cell in row if cell.strip())       
          # Append the count to the list
          non_null_counts.append(non_null_count)
          i+=1
    max_index = non_null_counts.index(max(non_null_counts))
    return(max_index)