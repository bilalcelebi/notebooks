import sqlite3
from sqlite3 import Error
import os
import pandas as pd

## First create a database and give the main method database name with .db
## Second give a table_name for creating table
## AND Ta Da! Table Created from CSV and all data inserted but there migth
## some losing

def create_connection(database_file):

    connection = None

    try:

        connection = sqlite3.connect(database_file)
        
        return connection

    except Error as e:

        print(e)

    
    return connection


def create_table(connection, sql):

    try:

        c = connection.cursor()
        c.execute(sql)

    except Error as e:

        print(e)


def insert_data(conn, table_name, data):

    sql = f"INSERT INTO {table_name} VALUES {str(data)}"
    
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
   
    print(cursor.lastrowid)

def main(data_path, database_name, table_name):

    df = pd.read_csv(data_path)
    df.dropna(inplace = True)
    
    response = []

    for idx,row in df.iterrows():
        
        pair = list()

        for col in df.columns:

            pair.append(row[col])
        
        response.append(tuple(pair))
            
    database = os.path.join(os.getcwd(), database_name)
    conn = create_connection(database)

    table_sql = f"""CREATE TABLE IF NOT EXISTS {table_name} ( """
    
    obj_cols = [col for col in df.columns if df[col].dtype == 'object' or df[col].dtype == 'bool']

    for col in obj_cols:

        df[col] = df[col].astype('string')
    
    float_cols = [col for col in df.columns if df[col].dtype == 'float64']
    
    for col in float_cols:

        df[col] = df[col].astype('int')
    

    idx = 0
    for col in df.columns:

        col_name = str(col)
        col_type = str(df[col].dtype)
        type_name = None

        if col_type == 'string':

            type_name = 'text'

        elif col_type == 'int64':

            type_name = 'integer'


        pair = f'{col_name} {type_name}'

        if idx < len(df.columns) - 1:

            pair += ','

        idx += 1
        
        table_sql += pair

    table_sql += ')'
    
    create_table(conn, table_sql)
    
    for pair in response:
        
        try:
            insert_data(conn, table_name, pair)
        except:
            pass


if __name__ == '__main__':

    main('/home/bilalcelebi/Workspace/notebooks/data/youtube-data/channels.csv', 'learning.db', 'csvtosql2')
