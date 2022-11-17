import pymysql
import os
from dotenv import load_dotenv

def connect():
    # Load environment variables from .env file
    load_dotenv()
    host = os.environ.get("mysql_host")
    user = os.environ.get("mysql_user")
    password = os.environ.get("mysql_pass")
    database = os.environ.get("mysql_db")

    # Establish a database connection
    connection = pymysql.connect(
        host,
        user,
        password,
        database
    )

    # A cursor is an object that represents a DB cursor,
    # which is used to manage the context of a fetch operation.
    return connection

#SELECT data into the table
def select(table, where=None, order=None):
    connection = connect()
    cursor = connection.cursor()
    #import pdb; pdb.set_trace()
    # Execute SQL query
    if not where and not order:
        cursor.execute(f'SELECT * FROM {table}')
    elif where and not order:
        cursor.execute(f'SELECT * FROM {table} WHERE {where}')
    elif not where and order:
        cursor.execute(f'SELECT * FROM {table} ORDER BY {order}')
    else:
        cursor.execute(f'SELECT * FROM {table} WHERE {where} ORDER BY {order}')    
    # Gets all rows from the result
    rows = cursor.fetchall()
    return rows

#INSERT data into the table
def insert(table, column, att):
    #import pdb; pdb.set_trace()
    insert = f'INSERT INTO {table} ({column}) VALUES ({att})'
    connection = connect()  # Getting from function connect to the connection of database
    cursor = connection.cursor()
    cursor.execute(insert) #Execute SQL query 
    connection.commit() #Makes a commit to the database.
    id = cursor.lastrowid
    return id

#UPDATE data into the table
def update(table, att, where):
    #import pdb; pdb.set_trace()
    update = f'UPDATE {table} SET {att} WHERE {where}'
    connection = connect()  # Getting from function connect to the connection of database
    cursor = connection.cursor()
    cursor.execute(update) #Execute SQL query 
    connection.commit() #Makes a commit to the database.

#DELETE data into the table
def delete_db (table, where):
    delete = f'DELETE FROM {table} WHERE {where}'
    connection = connect()  # Getting from function connect to the connection of database
    cursor = connection.cursor()
    cursor.execute(delete) #Execute SQL query 
    connection.commit() #Makes a commit to the database

def close():
    connect()
    # Closes the cursor so will be unusable from this point 
    cursor.close()

    # Closes the connection to the DB, make sure you ALWAYS do this
    connection.close()